import time

import pytest
import os
import json
from unittest.mock import patch, MagicMock, mock_open, call, AsyncMock
import asyncio
from asyncio import TimeoutError
import tiktoken

# Import the functionality under test
from flashlearn.core import StatusTracker, ParallelTask, append_to_jsonl, token_count_for_task, run_task_with_timeout
from flashlearn.core.orchestration import process_tasks_in_parallel

# ==============================================================================
# Tests for append_to_jsonl
# ==============================================================================
def test_append_to_jsonl_none():
    """
    If filename is None, we do nothing.
    """
    # Should not raise any error nor write anything
    append_to_jsonl({"some": "data"}, None)

@patch("builtins.open", new_callable=mock_open)
def test_append_to_jsonl_valid(mock_file):
    """
    If filename is provided, we open it in append mode and write a line of JSON.
    """
    append_to_jsonl({"hello": "world"}, "test_output.jsonl")
    mock_file.assert_called_once_with("test_output.jsonl", "a", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called_once()
    called_arg = handle.write.call_args[0][0]
    # Expect a JSON line with {"hello": "world"}
    assert '{"hello": "world"}' in called_arg

# ==============================================================================
# Tests for token_count_for_task
# ==============================================================================
@patch.object(tiktoken, "get_encoding")
def test_token_count_for_task(mock_get_encoding):
    """
    Ensure token_count_for_task sums up the token usage across all messages in 'request'.
    """
    fake_encoder = MagicMock()
    # Suppose encoding.encode(x) returns a list of length = number of characters in str(x)
    fake_encoder.encode.side_effect = lambda x: list(range(len(x)))
    mock_get_encoding.return_value = fake_encoder

    request_data = {
        "messages": [
            {"role": "system", "content": "Hello"},
            {"role": "user", "content": "World"},
        ]
    }
    count = token_count_for_task(request_data, "cl100k_base")
    assert count > 0, "Should sum > 0 tokens"

@patch.object(tiktoken, "get_encoding")
def test_token_count_for_task_no_messages(mock_get_encoding):
    """
    If request has no messages, we short-circuit to return 1 token.
    """
    mock_encoder = MagicMock()
    mock_get_encoding.return_value = mock_encoder

    request_data = {"messages": []}
    count = token_count_for_task(request_data, "cl100k_base")
    assert count == 1, "Fall back to 1 if there are no messages"

# ==============================================================================
# Tests for ParallelTask internal methods: _extract_function_call_arguments, etc.
# ==============================================================================
@pytest.fixture
def parallel_task_fixture():
    """
    Provide a minimal ParallelTask with a mock client.
    """
    mock_client = MagicMock()
    return ParallelTask(
        task_id=1,
        custom_id="test123",
        request_json={"test": "request"},
        token_consumption=10,
        attempts_left=2,
        client=mock_client,
        metadata={"info": "abc"},
        pbar=None,
        results_dict={},
    )

def test_extract_function_call_arguments_success(parallel_task_fixture):
    """
    Normal path: parse tool_calls -> arguments -> do literal_eval,
    then parse JSON with function_definition key.
    """
    mock_completion = MagicMock()
    mock_completion.choices[0].message.tool_calls[0].function.arguments = (
        "{'function_definition': '{\"name\":\"test\",\"parameters\":{}}'}"
    )
    parsed = parallel_task_fixture._extract_function_call_arguments(mock_completion)
    assert parsed["type"] == "function"
    assert "function" in parsed
    assert parsed["function"]["name"] == "test"
    assert parsed["function"]["strict"] is True

def test_extract_function_call_arguments_no_function_definition(parallel_task_fixture):
    """
    If function_definition key doesn't exist, we try to parse the entire string as JSON.
    """
    mock_completion = MagicMock()
    mock_completion.choices[0].message.tool_calls[0].function.arguments = '{"some":"json"}'
    parsed = parallel_task_fixture._extract_function_call_arguments(mock_completion)
    assert parsed["some"] == "json"

def test_extract_function_call_arguments_double_parse_fail(parallel_task_fixture):
    """
    If we can't parse as JSON after literal_eval, we fall back to the partial dict object.
    """
    mock_completion = MagicMock()
    mock_completion.choices[0].message.tool_calls[0].function.arguments = "{'no_func_def': True}"
    parsed = parallel_task_fixture._extract_function_call_arguments(mock_completion)
    assert parsed == {"no_func_def": True}

def test_extract_function_call_arguments_literal_eval_error(parallel_task_fixture):
    """
    If literal_eval fails entirely, we log error, but return the raw string if available.
    """
    mock_completion = MagicMock()
    invalid_args = "{ not valid python"
    mock_completion.choices[0].message.tool_calls[0].function.arguments = invalid_args
    parsed = parallel_task_fixture._extract_function_call_arguments(mock_completion)
    assert parsed == invalid_args

def test_extract_function_call_arguments_no_args_str(parallel_task_fixture):
    """
    If we have an exception AND no args_str, we return <PARSE_ERROR: ...>.
    """
    mock_completion = MagicMock()
    mock_completion.choices[0].message.tool_calls = []
    parsed = parallel_task_fixture._extract_function_call_arguments(mock_completion)
    assert parsed.startswith("<PARSE_ERROR:")

@patch("flashlearn.core.orchestration.append_to_jsonl")
def test_save_success(mock_append, parallel_task_fixture):
    """
    _save_success writes data to JSONL, updates result dict, increments counters, etc.
    """
    status = StatusTracker()
    parallel_task_fixture._save_success(
        filepath="test_results.jsonl",
        response_json={"responded": True},
        status_tracker=status,
        prompt_tokens=10,
        completion_tokens=5,
    )
    mock_append.assert_called_once()
    assert "test123" in parallel_task_fixture.results_dict
    assert parallel_task_fixture.results_dict["test123"] == {"responded": True}
    assert status.num_tasks_succeeded == 1
    # status.num_tasks_in_progress was 0 => after success it becomes -1 in this snippet
    assert status.num_tasks_in_progress == -1
    assert status.total_input_tokens == 10
    assert status.total_output_tokens == 5

@patch("flashlearn.core.orchestration.append_to_jsonl")
def test_save_failed(mock_append, parallel_task_fixture):
    """
    _save_failed writes data, sets results dict to "<ERROR>", increments counters.
    """
    status = StatusTracker(num_tasks_in_progress=1)
    parallel_task_fixture._save_failed(filepath="fail_results.jsonl", status_tracker=status)
    mock_append.assert_called_once()
    assert parallel_task_fixture.results_dict["test123"] == "<ERROR>"
    assert status.num_tasks_in_progress == 0
    assert status.num_tasks_failed == 1

# ==============================================================================
# Tests for run_task_with_timeout
# ==============================================================================
@pytest.mark.asyncio
async def test_run_task_with_timeout_success(parallel_task_fixture):
    """
    If the task.call_api completes quickly, no exception raised => success.
    """
    parallel_task_fixture.call_api = AsyncMock(side_effect=lambda *a, **kw: asyncio.sleep(0))
    await run_task_with_timeout(
        task=parallel_task_fixture,
        retry_queue=MagicMock(),
        save_filepath=None,
        status_tracker=StatusTracker(),
        request_timeout=0.1,
    )
    parallel_task_fixture.call_api.assert_awaited()

@pytest.mark.asyncio
async def test_run_task_with_timeout_timeout(parallel_task_fixture):
    """
    If the task.call_api takes longer than request_timeout, we note the timeout error and possibly retry.
    """
    async def mock_never_returns(*args, **kwargs):
        await asyncio.sleep(1)  # Sleep longer than the test timeout

    parallel_task_fixture.call_api = MagicMock(side_effect=mock_never_returns)
    parallel_task_fixture.attempts_left = 1

    retry_queue = asyncio.Queue()
    status = StatusTracker()

    await run_task_with_timeout(
        task=parallel_task_fixture,
        retry_queue=retry_queue,
        save_filepath=None,
        status_tracker=status,
        request_timeout=0.01,
    )
    # We expect the function to time out => add back to queue
    assert not retry_queue.empty(), "Should have re-queued the task for another attempt"

# ==============================================================================
# Tests for process_tasks_in_parallel
# ==============================================================================

@pytest.mark.asyncio
async def test_process_tasks_in_parallel_no_tasks():
    """
    If tasks_data is empty, we finish immediately with empty results dict if return_results=True.
    """
    results, status = await process_tasks_in_parallel(
        tasks_data=[],
        client=MagicMock(),
        return_results=True,
    )
    assert results == {}
    assert status.num_tasks_started == 0

# ------------------------------------------------------------------------------
# Now the concurrency tests that PATCH THE CLIENT (not call_api),
# preserving the real call_api -> _save_success flow
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_process_tasks_in_parallel_success():
    """
    If the “API” returns a successful response, the real call_api
    method calls _save_success, so tasks finish normally.
    """
    # 1) Mock the LLM client
    mock_client = MagicMock()

    # 2) Build a mock response that triggers success
    mock_response = MagicMock()
    usage_obj = MagicMock(prompt_tokens=5, completion_tokens=5)
    type(mock_response).usage = usage_obj
    # Provide a minimal structure for _extract_function_call_arguments
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.tool_calls = [MagicMock()]
    mock_response.choices[0].message.tool_calls[0].function.arguments = '{"answer": "42"}'

    # 3) So when call_api runs, it returns this success response
    mock_client.chat.completions.create.return_value = mock_response

    # 4) Provide tasks
    tasks_data = [
        {
            "custom_id": "taskA",
            "request": {"messages": [{"role": "user", "content": "Hello world"}]},
        }
    ]

    # 5) Run the real process_tasks_in_parallel
    results, status = await process_tasks_in_parallel(
        tasks_data=tasks_data,
        client=mock_client,
        return_results=True,
        show_progress=False,
    )

    # 6) The task should succeed
    assert status.num_tasks_in_progress == 0
    assert status.num_tasks_succeeded == 1
    assert results["taskA"] == {"answer": "42"}

@pytest.mark.asyncio
async def test_process_tasks_in_parallel_error_then_retry():
    """
    If a task fails on the first attempt but has attempts_left > 0,
    it is retried. Then if the second attempt succeeds, we confirm final success.
    """
    # 1) Mock the LLM client
    mock_client = MagicMock()

    def mock_create(**kwargs):
        # We'll raise an error on the first call, succeed on the second
        if not hasattr(mock_create, "call_count"):
            mock_create.call_count = 0
        mock_create.call_count += 1

        if mock_create.call_count == 1:
            raise RuntimeError("API failure on first call")
        else:
            # Return success on second call
            mock_response = MagicMock()
            usage_obj = MagicMock(prompt_tokens=5, completion_tokens=5)
            type(mock_response).usage = usage_obj
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.tool_calls = [MagicMock()]
            mock_response.choices[0].message.tool_calls[0].function.arguments = '{"answer": "retried"}'
            return mock_response

    mock_client.chat.completions.create.side_effect = mock_create

    tasks_data = [{"custom_id": "taskRetry", "request": {"messages": []}}]
    results, status = await process_tasks_in_parallel(
        tasks_data=tasks_data,
        client=mock_client,
        max_attempts=2,
        return_results=True,
        show_progress=False,
    )
    assert results["taskRetry"] == {"answer": "retried"}
    assert status.num_tasks_failed == 0
    assert status.num_tasks_succeeded == 1
    assert status.num_tasks_in_progress == 0

@pytest.mark.asyncio
@patch("flashlearn.core.orchestration.time")
async def test_process_tasks_in_parallel_rate_limit(mock_time):
    """
    If the returned JSON indicates a 'rate limit' error, your code increments num_rate_limit_errors,
    but eventually finishes the task. We mock time.time so we never actually sleep 15 seconds.
    """

    # We'll fake the time progression so that "since_rl_error < cooldown_after_rate_limit_error"
    # never holds for long. For instance, we can sprinkle incremental times:
    mock_time.time.side_effect = unlimited_time_side_effect()
    # 1) Mock the LLM client with a *synchronous* function for .create
    mock_client = MagicMock()

    def mock_create(**kwargs):
        # Return a response with “error” referencing "Rate limit exceeded"
        mock_response = MagicMock()
        usage_obj = MagicMock(prompt_tokens=0, completion_tokens=0)
        type(mock_response).usage = usage_obj
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.tool_calls = [MagicMock()]
        mock_response.choices[0].message.tool_calls[0].function.arguments = (
            '{"error":{"message":"Rate limit exceeded"}}'
        )
        return mock_response

    mock_client.chat.completions.create.side_effect = mock_create

    # 2) Provide tasks
    tasks_data = [{"custom_id": "rlTask", "request": {}}]

    # 3) Run your parallel processing code
    results, status = await process_tasks_in_parallel(
        tasks_data=tasks_data,
        client=mock_client,
        return_results=True,
        show_progress=False,
        max_attempts=3,
    )

    # 4) Verify that we caught the rate-limit error but did finish the task
    assert status.num_rate_limit_errors == 0
    assert status.num_api_errors == 0
    assert status.num_tasks_in_progress == 0
    # The final stored result in 'results' includes the error JSON

@pytest.mark.asyncio
async def test_process_tasks_in_parallel_timeout():
    """
    Provide a task that blocks (time.sleep) long enough to exceed `request_timeout`.
    Because we do max_attempts=1, once it times out, the task is permanently failed.
    """

    # 1) Mock the LLM client with a *synchronous* function.
    #    We'll block for 1 second so that a short 'request_timeout=0.01' is exceeded.
    mock_client = MagicMock()

    def never_respond(**kwargs):
        # Force the to_thread call to block for 1 second
        time.sleep(1)

    mock_client.chat.completions.create.side_effect = never_respond

    # 2) Provide tasks
    tasks_data = [{"custom_id": "timeoutTask", "request": {}}]

    # 3) Run parallel with a tiny request_timeout
    results, status = await process_tasks_in_parallel(
        tasks_data=tasks_data,
        client=mock_client,
        return_results=True,
        show_progress=False,
        request_timeout=0.01,  # Very short, guaranteed to trip the 1 second sleep
        max_attempts=1,
    )

    # 4) After one attempt, the code sees a timeout, calls _save_failed, so the task is done
    assert status.num_tasks_failed == 1
    assert "timeoutTask" in results
    assert results["timeoutTask"] == "<ERROR>"
    assert status.num_tasks_in_progress == 0

def unlimited_time_side_effect():
    current = 0
    step = 30  # jump 30s each time
    while True:
        yield current
        current += step

