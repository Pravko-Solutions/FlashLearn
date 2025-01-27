import argparse
import ast
import asyncio
import json
import logging
import os
import re
import time
from asyncio import TimeoutError, wait_for
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List, Union, Callable, Tuple

import tiktoken
from tqdm import tqdm

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("ParallelProcessor")

# ─────────────────────────────────────────────────────────────────────
# Custom exceptions to classify different error types
# ─────────────────────────────────────────────────────────────────────
class ApiError(Exception):
    """Base class for all API-related errors."""

class ApiAuthError(ApiError):
    """Authentication/authorization error (e.g., 401/403)."""

class ApiRateLimitError(ApiError):
    """Rate limit exceeded (e.g., 429)."""

class ApiServerError(ApiError):
    """Server-side error (e.g., 500/503)."""

class ApiUnrecoverableError(ApiError):
    """Any other error we can't or don't want to retry."""


# ─────────────────────────────────────────────────────────────────────
# Function that checks for presence of "error" in the response JSON
# and raises an appropriate exception if found.
# ─────────────────────────────────────────────────────────────────────
def analyze_response_for_errors(response_json: Dict[str, Any]) -> None:
    if "error" not in response_json:
        return

    err_obj = response_json["error"]
    code = err_obj.get("code")
    message = err_obj.get("message", "Unknown error.")

    if not isinstance(code, int):
        # If no numeric code or unexpected format => treat as unrecoverable
        raise ApiUnrecoverableError(f"Unknown API error: {message}")

    if code in (401, 403):
        raise ApiAuthError(f"{code} - {message}")
    elif code == 429:
        raise ApiRateLimitError(f"{code} - {message}")
    elif code in (500, 503):
        raise ApiServerError(f"{code} - {message}")
    else:
        raise ApiUnrecoverableError(f"{code} - {message}")


@dataclass
class StatusTracker:
    """
    Tracks global statistics and usage for the orchestrated parallel processing run.
    """
    num_tasks_started: int = 0
    num_tasks_in_progress: int = 0
    num_tasks_succeeded: int = 0
    num_tasks_failed: int = 0
    num_rate_limit_errors: int = 0
    num_api_errors: int = 0
    num_other_errors: int = 0
    time_of_last_rate_limit_error: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0


def append_to_jsonl(data: Any, filename: Optional[str]) -> None:
    """
    Appends a single JSON-serializable item to a JSON Lines file.
    Each call writes exactly one line in JSON. If 'filename' is None,
    the function is a no-op.
    """
    if filename is None:
        return
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


@dataclass
class ParallelTask:
    """
    Represents the data and metadata for one parallelizable request (task).
    """
    task_id: int
    custom_id: str
    request_json: dict
    token_consumption: int
    attempts_left: int
    client: Any
    metadata: Optional[dict] = field(default_factory=dict)
    pbar: Optional[tqdm] = None
    results_dict: Optional[Dict[str, Any]] = None
    result: List[Union[str, dict]] = field(default_factory=list)

    def _extract_function_call_arguments(self, completion: Any) -> Any:
        """
        Extracts JSON arguments from the model's function call (if present).
        Adjust as needed for your particular model response shape.
        """
        args_str = ''
        try:
            args_str = completion.choices[0].message.tool_calls[0].function.arguments
            args_obj = ast.literal_eval(args_str)
            try:
                # Possibly the function_definition is a JSON string
                args_obj = json.loads(args_obj['function_definition'])
                args_obj["strict"] = True
                return {"type": "function", "function": args_obj}
            except:
                # Or parse the entire string as JSON
                try:
                    args_obj = json.loads(args_str)
                except:
                    pass
                return args_obj
        except Exception as e:
            if args_str:
                return args_str
            logger.error(f"Error parsing function call arguments: {e}")
            return f"<PARSE_ERROR: {e}>"

    async def call_api(
        self,
        retry_queue: asyncio.Queue,
        save_filepath: Optional[str],
        status_tracker: "StatusTracker",
    ) -> None:
        """
        Invokes the client API in a separate thread, checks for known error codes,
        and re-queues on retryable failures.
        """
        logger.debug(
            f"Starting task #{self.task_id} with attempts_left={self.attempts_left}"
        )
        error_data = None
        try:
            # 1) Perform synchronous API call in a thread
            response = await asyncio.to_thread(
                self.client.chat.completions.create, **self.request_json
            )

            # 2) Check for error in the response (raises exception if found)
            analyze_response_for_errors(response)

            # 3) Retrieve usage data (if provided)
            try:
                usage_data = response.usage
                prompt_tokens = usage_data.prompt_tokens
                completion_tokens = usage_data.completion_tokens
            except:
                prompt_tokens = 0
                completion_tokens = 0

            # 4) Extract the essential data from the completion
            response_json = self._extract_function_call_arguments(response)

            # 5) Success path => record success
            self._save_success(
                filepath=save_filepath,
                response_json=response_json,
                status_tracker=status_tracker,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            return

        except ApiRateLimitError as e:
            # 429 => we can retry with backoff
            logger.warning(f"Task {self.task_id} hit rate limit: {e}")
            status_tracker.num_rate_limit_errors += 1
            status_tracker.time_of_last_rate_limit_error = time.time()
            error_data = str(e)

        except ApiServerError as e:
            # 5xx => also retryable
            logger.warning(f"Task {self.task_id} saw a server error: {e}")
            status_tracker.num_api_errors += 1
            error_data = str(e)

        except ApiAuthError as e:
            # 401/403 => cannot retry; fail permanently
            logger.error(
                f"Authentication/authorization error for task {self.task_id}: {e}"
            )
            status_tracker.num_api_errors += 1
            error_data = str(e)
            self.result.append(error_data)
            self._save_failed(save_filepath, status_tracker)
            return

        except ApiUnrecoverableError as e:
            # Some other known code => no point retrying
            logger.error(f"Unrecoverable error for task {self.task_id}: {e}")
            status_tracker.num_api_errors += 1
            error_data = str(e)
            self.result.append(error_data)
            self._save_failed(save_filepath, status_tracker)
            return

        except Exception as e:
            # Any unexpected exception => we can try again if attempts_left
            logger.error(f"Task {self.task_id} faced an unknown exception: {e}")
            status_tracker.num_other_errors += 1
            error_data = str(e)

        # If we got here, we have a retryable situation (rate-limit, server, or unknown).
        self.result.append(error_data)
        if self.attempts_left > 0:
            # Exponential backoff approach: store incrementing backoff attempt
            backoff_count = self.metadata.get("backoff_attempt", 0) + 1
            self.metadata["backoff_attempt"] = backoff_count
            delay = min(2 ** backoff_count, 60)  # up to 60s
            self.metadata["next_allowed_time"] = time.time() + delay
            retry_queue.put_nowait(self)
        else:
            logger.error(
                f"Task {self.task_id} permanently failed after all retries. Error: {error_data}"
            )
            self._save_failed(save_filepath, status_tracker)


    def _save_success(
        self,
        filepath: Optional[str],
        response_json: dict,
        status_tracker: "StatusTracker",
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
    ) -> None:
        """
        Records a successful result both in JSONL (if filepath is given) and in memory.
        """
        data = (
            [self.request_json, response_json, self.metadata]
            if self.metadata
            else [self.request_json, response_json]
        )
        append_to_jsonl(data, filepath)

        # Store result if we have a shared dict
        if self.results_dict is not None:
            cid = self.custom_id or str(self.task_id)
            self.results_dict[cid] = response_json

        status_tracker.num_tasks_succeeded += 1
        status_tracker.num_tasks_in_progress -= 1
        status_tracker.total_input_tokens += prompt_tokens
        status_tracker.total_output_tokens += completion_tokens

        if self.pbar is not None:
            self.pbar.set_postfix_str(
                f"In total: {status_tracker.total_input_tokens}, "
                f"Out total: {status_tracker.total_output_tokens}"
            )
            self.pbar.update(1)

    def _save_failed(self, filepath: Optional[str], status_tracker: "StatusTracker") -> None:
        """
        Records a permanently failed result in JSONL (if filepath is given) and updates counters.
        """
        data = (
            [self.request_json, self.result, self.metadata]
            if self.metadata
            else [self.request_json, self.result]
        )
        append_to_jsonl(data, filepath)

        # Mark result as <ERROR> in shared dict
        if self.results_dict is not None:
            cid = self.custom_id or str(self.task_id)
            self.results_dict[cid] = "<ERROR>"

        status_tracker.num_tasks_in_progress -= 1
        status_tracker.num_tasks_failed += 1

        if self.pbar is not None:
            self.pbar.update(1)


def token_count_for_task(task_data: dict, token_encoding_name: str = "cl100k_base") -> int:
    """
    Estimates how many tokens this request might consume.
    Adjust logic to match your actual request + token counting approach.
    """
    encoding = tiktoken.get_encoding(token_encoding_name)
    messages = task_data.get("messages", [])
    total_tokens = 0
    for msg in messages:
        total_tokens += len(encoding.encode(str(msg)))
    return total_tokens or 1


def task_id_generator():
    """
    A simple infinite generator for task IDs: 0, 1, 2, 3, ...
    """
    current = 0
    while True:
        yield current
        current += 1


async def run_task_with_timeout(
    task: ParallelTask,
    retry_queue: asyncio.Queue,
    save_filepath: Optional[str],
    status_tracker: StatusTracker,
    request_timeout: float
) -> None:
    """
    Invokes task.call_api(...) with an overall timeout.
    """
    try:
        await wait_for(
            task.call_api(
                retry_queue=retry_queue,
                save_filepath=save_filepath,
                status_tracker=status_tracker
            ),
            timeout=request_timeout,
        )
    except TimeoutError:
        error_str = f"Request timed out after {request_timeout} seconds."
        task.result.append(error_str)
        if task.attempts_left > 0:
            task.metadata["backoff_attempt"] = task.metadata.get("backoff_attempt", 0) + 1
            delay = min(2 ** task.metadata["backoff_attempt"], 60)
            task.metadata["next_allowed_time"] = time.time() + delay
            retry_queue.put_nowait(task)
        else:
            logger.error(f"Task {task.task_id} permanently failed due to timeout.")
            task._save_failed(save_filepath, status_tracker)


async def process_tasks_in_parallel(
    tasks_data: List[dict],
    client: Any,
    max_requests_per_minute: float = 1000,
    max_tokens_per_minute: float = 1000000,
    max_attempts: int = 3,
    token_encoding_name: str = "cl100k_base",
    logging_level: int = logging.INFO,
    save_filepath: Optional[str] = None,
    show_progress: bool = True,
    return_results: bool = True,
    request_timeout: float = 5.0,
) -> Tuple[Optional[Dict[str, Any]], StatusTracker]:
    """
    Main orchestrator for concurrent tasks with rate-limiting, retry,
    concurrency control, and optional result capture.

    • We handle known error codes and do exponential backoff for 429/5xx.
    • If no headers are present, we use defaults as normal.
    """
    if max_requests_per_minute > 1000 or max_tokens_per_minute > 1000000 or max_attempts > 3:
        raise EnterpriseVersionRequiredError()

    logger.setLevel(logging_level)
    max_queue_size = 2000
    seconds_to_sleep_each_loop = 0.0001
    cooldown_after_rate_limit_error = 15

    # Prepare concurrency and status tracking
    status = StatusTracker()
    retry_queue = asyncio.Queue()
    next_id = task_id_generator()
    results_out: Optional[Dict[str, Any]] = {} if return_results else None

    pbar = tqdm(
        total=len(tasks_data),
        desc="Processing tasks - For consulting and support visit: https://calendly.com/flashlearn",
        disable=not show_progress,
    )

    # We'll enqueue tasks incrementally
    tasks_queue = asyncio.Queue()

    i = 0
    n = len(tasks_data)

    def load_tasks_into_queue():
        nonlocal i
        while i < n and tasks_queue.qsize() < max_queue_size:
            raw_item = tasks_data[i]
            request_json = raw_item.get("request", {})
            meta = raw_item.get("metadata", {})
            custom_id = raw_item.get("custom_id")
            if not custom_id:
                custom_id = f"auto_{next(next_id)}"

            # Count tokens
            tokens = token_count_for_task(request_json, token_encoding_name)
            new_task = ParallelTask(
                task_id=next(next_id),
                custom_id=custom_id,
                request_json=request_json,
                token_consumption=tokens,
                attempts_left=max_attempts,
                client=client,
                metadata=meta,
                pbar=pbar,
                results_dict=results_out,
            )
            tasks_queue.put_nowait(new_task)
            status.num_tasks_started += 1
            status.num_tasks_in_progress += 1
            i += 1

    # Start available capacities at 0, so they build over time
    available_req_capacity = 0.0
    available_token_capacity = 0.0
    last_update_time = time.time()

    while True:
        # 1) Load more tasks if there's room
        load_tasks_into_queue()

        # 2) Pick a pending task (retry first, then new tasks), if any
        pending_task: Optional[ParallelTask] = None

        if not retry_queue.empty():
            candidate = retry_queue.get_nowait()
            next_allowed = candidate.metadata.get("next_allowed_time", 0.0)
            if time.time() >= next_allowed:
                pending_task = candidate
            else:
                retry_queue.put_nowait(candidate)
        elif not tasks_queue.empty():
            candidate = tasks_queue.get_nowait()
            next_allowed = candidate.metadata.get("next_allowed_time", 0.0)
            if time.time() >= next_allowed:
                pending_task = candidate
            else:
                tasks_queue.put_nowait(candidate)

        # 3) Figure out how much time has passed, and refill capacity
        now = time.time()
        dt = now - last_update_time
        last_update_time = now

        # Concurrency is fixed to the user-provided rate (no dynamic changes)
        current_req_per_minute = max_requests_per_minute
        current_tokens_per_minute = max_tokens_per_minute

        # Refill request capacity
        available_req_capacity = min(
            available_req_capacity + (current_req_per_minute * dt / 60.0),
            current_req_per_minute,
        )
        # Refill token capacity
        available_token_capacity = min(
            available_token_capacity + (current_tokens_per_minute * dt / 60.0),
            current_tokens_per_minute,
        )

        # 4) If there's a pending task and enough capacity, schedule it
        if pending_task:
            if (
                available_req_capacity >= 1
                and available_token_capacity >= pending_task.token_consumption
            ):
                available_req_capacity -= 1
                available_token_capacity -= pending_task.token_consumption
                pending_task.attempts_left -= 1
                asyncio.create_task(
                    run_task_with_timeout(
                        task=pending_task,
                        retry_queue=retry_queue,
                        save_filepath=save_filepath,
                        status_tracker=status,
                        request_timeout=request_timeout,
                    )
                )
            else:
                # Not enough capacity, return it to the queue for later
                await tasks_queue.put(pending_task)

        # 5) Check if we're fully done
        all_enqueued = (i >= n)
        if (all_enqueued and status.num_tasks_in_progress == 0
                and tasks_queue.empty() and retry_queue.empty()):
            break

        # 6) Sleep a tiny bit so we don't spin the loop too hard
        await asyncio.sleep(seconds_to_sleep_each_loop)

        # 7) If a rate-limit error was hit recently, apply a cooldown
        since_rl_error = time.time() - status.time_of_last_rate_limit_error
        if (
            since_rl_error < cooldown_after_rate_limit_error
            and status.num_rate_limit_errors > 0
        ):
            to_sleep = cooldown_after_rate_limit_error - since_rl_error
            logger.warning(
                f"Pausing {int(to_sleep)}s to cool down after rate-limit error."
            )
            await asyncio.sleep(to_sleep)

    pbar.close()
    logger.info(
        f"All tasks complete. {status.num_tasks_succeeded} succeeded, "
        f"{status.num_tasks_failed} failed."
        + (f" Results saved to {save_filepath}" if save_filepath else "")
    )

    if status.num_rate_limit_errors > 0:
        logger.warning(
            f"Encountered {status.num_rate_limit_errors} rate-limit errors. "
            "Consider lowering your request rate or using larger request batches."
        )

    if return_results and results_out is not None:
        return results_out, status
    return None, status

class EnterpriseVersionRequiredError(Exception):
    def __init__(self, message="Enterprise version required for more than 1000 requests per minute. Request a demo at https://calendly.com/flashlearn/enterprise-demo"):
        super().__init__(message)