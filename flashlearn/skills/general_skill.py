import logging
from typing import Dict, Any, List

from copy import copy
import ast
import json

from flashlearn.core import FlashLiteLLMClient
from flashlearn.skills.base_data_skill import BaseDataSkill

flash_logger = logging.getLogger("FlashLearn")
logging.basicConfig(level=logging.ERROR)


class GeneralSkill(BaseDataSkill):
    """
    A general-purpose skill that accepts a custom function definition at init.
    Overrides only the pieces that differ from the default base logic.

    This version expects its data input as a list of dictionaries (one dict per row).
    """

    def __init__(
            self,
            model_name: str,
            function_definition: Dict[str, Any],
            system_prompt: str = "You are a helpful assistant.",
            columns: List[str] = None,
            client=FlashLiteLLMClient()
    ):
        super().__init__(model_name=model_name, system_prompt=system_prompt, client=client)
        self._function_definition = function_definition
        self.columns = columns or []

    def create_tasks(
            self,
            df: List[Dict[str, Any]],
            column_modalities: Dict[str, str] = None,
            output_modality: str = "text",
            columns: List[str] = None,
            **kwargs
    ) -> List[Dict[str, Any]]:
        """
        If the user doesn't pass a 'columns' list, we fall back
        to self.columns if available. Then pass on to the parent
        create_tasks (BaseDataSkill) which handles the logic of converting
        each dict into blocks.

        :param df: A list of dicts to process (one dict per row).
        :param column_modalities: Mapping key->modality (e.g. text, image_url, etc.)
        :param output_modality: "text", "audio", or "image" for the model's response.
        :param columns: (Optional) Not used by default logic, but present for consistency.
        :param kwargs: Additional arguments if needed.
        :return: A list of tasks for parallel processing.
        """
        if not columns:
            columns = self.columns

        return super().create_tasks(
            df=df,
            column_modalities=column_modalities,
            output_modality=output_modality,
            columns=columns,
            **kwargs
        )

    def _build_function_def(self) -> Dict[str, Any]:
        """
        Return whatever custom function definition was provided at init.
        """
        return self._function_definition

    def parse_result(self, raw_result: Dict[str, Any]) -> Any:
        """
        By default, just returns the raw result.
        Override this if you need more complex parsing.
        """
        return raw_result

    @staticmethod
    def load_skill(config: Dict[str, Any], model_name="gpt-4o-mini",client=FlashLiteLLMClient()):
        """
        Load a dictionary specifying model, prompts, and function definition, then
        return an initialized GeneralSkill instance.

        Example config structure:
          {
            "skill_class": "GeneralSkill",
            "model_name": "gpt-4o",
            "system_prompt": "Exactly populate the provided function definition",
            "function_definition": {
              "type": "function",
              "function": {
                "name": "text_classification",
                "description": "Classify text into categories.",
                "strict": true,
                "parameters": { ... }
              }
            },
            "columns": ["some_column", "another_column"]
          }
        """
        model_name = model_name
        system_prompt = config.get("system_prompt", "You are a helpful assistant.")
        function_definition = config.get("function_definition", {})
        columns = config.get("columns", [])

        return GeneralSkill(
            model_name=model_name,
            function_definition=function_definition,
            system_prompt=system_prompt,
            columns=columns,
            client=client
        )