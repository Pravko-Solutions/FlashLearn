from typing import Dict, Any, List
from flashlearn.core import FlashLiteLLMClient
from flashlearn.skills.base_data_skill import BaseDataSkill

class ClassificationSkill(BaseDataSkill):
    """
    A skill that classifies text from each input dictionary into one or more known categories.
    Optionally set max_categories = -1 if you want unlimited picks.
    """

    def __init__(
        self,
        model_name: str,
        categories: List[str],
        max_categories: int = 1,
        system_prompt: str = "",
        client=FlashLiteLLMClient()
    ):
        super().__init__(model_name=model_name, system_prompt=system_prompt, client=client)
        self.categories = categories
        self.max_categories = max_categories

    def _build_function_def(self) -> Dict[str, Any]:
        """
        Overridden to produce a JSON schema requiring “categories”.
        If max_categories == 1, we expect a single string category.
        Otherwise, we allow an array of category strings.
        """
        if self.max_categories == 1:
            prop_def = {
                "type": "string",
                "enum": self.categories,
                "description": "A chosen category from the provided set."
            }
        else:
            prop_def = {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": self.categories
                },
                "description": "A list of chosen categories from the provided set."
            }
            if self.max_categories > 0:
                prop_def["maxItems"] = self.max_categories

        return {
            "type": "function",
            "function": {
                "name": "categorize_text",
                "description": (
                    f"Classify text into up to {self.max_categories} categories from a given list."
                    if self.max_categories != 1
                    else f"Classify text into exactly 1 category out of {self.categories}."
                ),
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "categories": prop_def
                    },
                    "required": ["categories"],
                    "additionalProperties": False
                }
            }
        }

    def parse_result(self, raw_result: Dict[str, Any]) -> Any:
        """
        Extract the 'categories' result we specified in the function schema.
        Returns a list of categories (even if only one was chosen).
        """
        categories_ret = self.parse_function_call(raw_result, arg_name="categories")
        if not categories_ret:
            return []
        # If the schema was string for single-cat, convert to list
        if isinstance(categories_ret, str):
            return [categories_ret]
        return categories_ret