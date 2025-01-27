"""
Initialize the 'core' subpackage of FlashLearn.

This file ensures 'core' is recognized as a subpackage.
You can expose certain classes/functions here if desired.
"""

# Example of importing necessary modules from the subpackage:
from .flash_client import FlashLiteLLMClient
from .orchestration import StatusTracker, ParallelTask, append_to_jsonl, token_count_for_task, run_task_with_timeout, \
    process_tasks_in_parallel

__all__ = [
     'FlashLiteLLMClient',
]