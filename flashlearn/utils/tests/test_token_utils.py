import pytest

from flashlearn.utils.token_utils import _count_tokens_for_messages, _count_tokens_for_function_defs, \
    count_tokens_for_task, count_tokens_for_tasks


@pytest.mark.parametrize("messages,expected_min_tokens", [
    (
        [
            {"role": "system", "content": "Hello, I am the system message."},
            {"role": "user", "content": "Tell me a story please."}
        ],
        1
    ),
    (
        [
            {"role": "user", "content": "Short prompt."}
        ],
        1
    ),
    ([], 0),
])
def test_count_tokens_for_messages(messages, expected_min_tokens):
    """
    Basic tests for _count_tokens_for_messages using a known model name.
    We check that the token count is at least the expected_min_tokens.
    """
    model_name = "gpt-3.5-turbo"
    tokens = _count_tokens_for_messages(messages, model_name)
    # We primarily verify that the function doesn't crash and returns a numeric token count.
    assert isinstance(tokens, int)
    assert tokens >= expected_min_tokens


@pytest.mark.parametrize("function_defs,expected_min_tokens", [
    (
        [
            {
                "name": "test_function",
                "description": "A simple test function definition",
                "parameters": {"type": "object", "properties": {"test_prop": {"type": "string"}}}
            }
        ],
        1
    ),
    ([], 0),
    (
        [
            {"arbitrary": "Anything could be here."},
            {"second_def": 123}
        ],
        1
    ),
])
def test_count_tokens_for_function_defs(function_defs, expected_min_tokens):
    """
    Check that _count_tokens_for_function_defs produces a non-negative
    integer token count, and is at least expected_min_tokens.
    """
    model_name = "gpt-3.5-turbo"
    tokens = _count_tokens_for_function_defs(function_defs, model_name)
    assert isinstance(tokens, int)
    assert tokens >= expected_min_tokens


def test_count_tokens_for_task_basic():
    """
    Verify count_tokens_for_task sums tokens from both messages and functions.
    """
    task = {
        "custom_id": "123",
        "request": {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "System says hello."},
                {"role": "user", "content": "User asks a question."}
            ],
            "functions": [
                {"name": "dummy_function", "description": "Does something."}
            ]
        }
    }
    tokens = count_tokens_for_task(task, default_model="gpt-3.5-turbo")
    assert isinstance(tokens, int)
    assert tokens > 0, "Should count some tokens for both messages and function definitions."


def test_count_tokens_for_task_no_request_key():
    """
    If 'request' key is missing or empty, we should handle gracefully and get zero tokens.
    """
    task = {
        "custom_id": "no_request"
    }
    tokens = count_tokens_for_task(task, default_model="gpt-3.5-turbo")
    assert tokens == 0


def test_count_tokens_for_tasks_basic():
    """
    Confirm that count_tokens_for_tasks sums the token counts across multiple tasks.
    """
    tasks = [
        {
            "custom_id": "1",
            "request": {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello world"}],
                "functions": []
            }
        },
        {
            "custom_id": "2",
            "request": {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "assistant", "content": "Sure, here's a reply."}],
                "functions": [{"fun": "some definition"}]
            }
        }
    ]
    total_tokens = count_tokens_for_tasks(tasks, default_model="gpt-3.5-turbo")
    assert isinstance(total_tokens, int)
    # We can't predict exact tokens, but it should be > 0 if there's content in both tasks.
    assert total_tokens > 0


def test_count_tokens_for_tasks_empty():
    """
    If tasks is an empty list, total tokens should be 0.
    """
    empty_tasks = []
    total_tokens = count_tokens_for_tasks(empty_tasks, default_model="gpt-3.5-turbo")
    assert total_tokens == 0