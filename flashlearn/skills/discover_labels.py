from typing import List, Dict, Any
from flashlearn.core import FlashLiteLLMClient
from flashlearn.skills.base_data_skill import BaseDataSkill


class DiscoverLabelsSkill(BaseDataSkill):
    """
    Example of a skill that lumps all rows (dicts) together into a
    single user message for discovering labels across the entire dataset.
    """

    def __init__(
        self,
        model_name: str,
        label_count: int = -1,
        system_prompt: str = "",
        client=FlashLiteLLMClient()
    ):
        super().__init__(model_name=model_name, system_prompt=system_prompt, client=client)
        self.label_count = label_count

    def create_tasks(
        self,
        df: List[Dict[str, Any]],
        column_modalities: Dict[str, str] = None,
        output_modality: str = "text",
        columns: List[str] = None,  # Not really used, present for API consistency
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Instead of “one row = one task,” we produce “one big task” with
        all rows included as a single user message.
        :param df: A list of dicts (each dict = one row of data).
        :param column_modalities: Which keys get “text”, “image_url”, “audio”, etc.
        :param output_modality: "text", "audio", or "image" (passed to build_output_params).
        :param columns: Ignored here; kept for signature compatibility.
        :return: A single-item list containing one aggregated task, or empty if no content.
        """
        if output_modality != "text":
            output_params = self.build_output_params(output_modality)
        else:
            output_params = {}
        all_blocks = []

        # Aggregate content blocks across all rows
        for row in df:
            row_blocks = self.build_content_blocks(row, column_modalities)
            all_blocks.extend(row_blocks)

        if not all_blocks:
            return []

        flattened_str = self.flatten_blocks_for_debug(all_blocks)

        # Possibly mention the label_count in the prompt
        if self.label_count > 0:
            sys_prompt = (
                f"{self.system_prompt} You may select up to {self.label_count} labels."
            )
        else:
            sys_prompt = f"{self.system_prompt} You may select any number of labels."

        system_msg = {
            "role": "system",
            "content": sys_prompt,
            "content_str": sys_prompt
        }
        user_msg = {
            "role": "user",
            "content": all_blocks,
            "content_str": flattened_str
        }

        request_body = {
            "model": self.model_name,
            "messages": [system_msg, user_msg],
            "tools": [self._build_function_def()],
            "tool_choice": "required"
        }
        request_body.update(output_params)

        # Return just one aggregated task
        return [{
            "custom_id": "0",
            "request": request_body
        }]

    def _build_function_def(self) -> Dict[str, Any]:
        """
        Build a function definition that expects an array of strings labeled 'labels'.
        """
        prop_def = {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of label strings summarizing the entire dataset."
        }
        return {
            "type": "function",
            "function": {
                "name": "infer_labels",
                "description": "Infer some labels for an entire dataset.",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "labels": prop_def
                    },
                    "required": ["labels"],
                    "additionalProperties": False
                }
            }
        }

    def parse_result(self, raw_result: Dict[str, Any]) -> Any:
        """
        Parse the 'labels' key from function call arguments.
        Falls back to an empty list if not present.
        """
        return self.parse_function_call(raw_result, arg_name="labels") or []