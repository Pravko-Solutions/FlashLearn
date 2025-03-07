import asyncio
from abc import ABC, abstractmethod
import json
import os
from typing import List, Dict, Any

from flashlearn.core.flash_client import FlashLiteLLMClient
from flashlearn.core.orchestration import process_tasks_in_parallel
from flashlearn.utils.token_utils import count_tokens_for_tasks


class BaseSkill(ABC):
    """
    Abstract base for any 'skill' that FlashLearn can execute.
    Enforces a consistent interface for building tasks, parsing results,
    and building function definitions for function calling.

    NOTE: This version expects inputs as a list of dictionaries
    where each dictionary is treated as a "row" with key/value pairs
    corresponding to columns/fields. The default "column modality" is "text",
    but you can specify others as needed in child classes that implement
    create_tasks().
    """

    def __init__(self, model_name: str, system_prompt: str = '', full_row=False, client=FlashLiteLLMClient()):
        self.model_name = model_name
        self.client = client
        self.system_prompt = system_prompt
        self.full_row = full_row
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    @abstractmethod
    def create_tasks(self, df, **kwargs) -> List[Dict[str, Any]]:
        """
        Build a list of tasks for the given data, which is expected to be
        a list of dictionaries (df). Each dict is treated as one "row"
        containing key/value pairs for the data fields.
        """
        raise NotImplementedError()

    @abstractmethod
    def _build_function_def(self) -> Dict[str, Any]:
        """
        Return the function definition (with JSON schema) that the model will use.
        """
        raise NotImplementedError()

    def save(self, filepath: str = None):
        """
        Save this skill's function definition (and any relevant metadata) to JSON.

        :param filepath: Optional path. Defaults to <ClassName>.json in current directory.
        :return: The dictionary that was saved.

        NOTE: model_name is deliberately excluded from the saved JSON as requested.
        """
        if filepath is None:
            filepath = f"{self.__class__.__name__}.json"

        definition_out = {
            "skill_class": self.__class__.__name__,
            "system_prompt": self.system_prompt,
            "function_definition": self._build_function_def()
            # model_name is intentionally omitted
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(definition_out, f, indent=2)

        print(f"Skill definition saved to: {os.path.abspath(filepath)}")
        return definition_out

    def run_tasks_in_parallel(
            self,
            tasks: list,
            save_filepath: str = None,
            max_requests_per_minute=999,
            max_tokens_per_minute=999999,
            max_attempts=2,
            token_encoding_name="cl100k_base",
            return_results=True,
            request_timeout=60,
    ):
        """
        Orchestrates tasks in parallel using process_tasks_in_parallel.

        :param tasks: The list of tasks to run.
        :param save_filepath: Where to save partial progress or results (optional).
        :param max_requests_per_minute: Throttle for requests/min.
        :param max_tokens_per_minute: Throttle for tokens/min.
        :param max_attempts: How many times to attempt a failed request before giving up.
        :param token_encoding_name: The token encoding name (e.g., cl100k_base).
        :param return_results: Whether to return the final results.
        :param request_timeout: Timeout for each request.
        :return: (final_results, final_status_tracker).
        """
        final_results, final_status = asyncio.run(
            process_tasks_in_parallel(
                return_results=return_results,
                client=self.client,
                tasks_data=tasks,
                save_filepath=save_filepath,
                max_requests_per_minute=max_requests_per_minute,
                max_tokens_per_minute=max_tokens_per_minute,
                max_attempts=max_attempts,
                token_encoding_name=token_encoding_name,
                request_timeout=request_timeout,

            )
        )
        # Update usage statistics from the status tracker
        self.total_input_tokens = getattr(final_status, "total_input_tokens", 0)
        self.total_output_tokens = getattr(final_status, "total_output_tokens", 0)
        return final_results

    def estimate_tasks_cost(self, tasks: list) -> float:
        """
        Return an approximate cost of tasks, based on # tokens * rate.
        Adjust the rate to match your model's actual pricing.
        """
        total_tokens = count_tokens_for_tasks(tasks, self.model_name)
        # Example: GPT-4 prompt rate might be ~$0.03 / 1K tokens
        return total_tokens * 1.5