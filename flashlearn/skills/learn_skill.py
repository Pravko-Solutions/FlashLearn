import logging
from copy import copy
from typing import Dict, Any, List
import ast
import json

from flashlearn.core import FlashLiteLLMClient
from flashlearn.skills import GeneralSkill

flash_logger = logging.getLogger("FlashLearn")
logging.basicConfig(level=logging.ERROR)

class LearnSkill:
    """
    Orchestrator class for:
     - Managing a FlashClient
     - Concurrency for tasks
     - Batch submission logic
     - Cost estimation
     - Creating or retrieving skill objects
     - Additional utility like "learn_skill"
    """

    def __init__(
        self,
        model_name: str = "gpt-4o",
        verbose: bool = True,
        client=FlashLiteLLMClient()
    ):
        flash_logger.setLevel(logging.INFO if verbose else logging.ERROR)
        flash_logger.info(f"Initializing FlashLearn with model '{model_name}'.")
        self.client = client
        self.model_name = model_name
        self.verbose = verbose

    def learn_skill(
        self,
        df: List[Dict[str, Any]],
        task: str = "",
        columns: List[str] = None,
        model_name: str = "gpt-4o-mini",
        column_modalities: Dict[str, str] = None,
        output_modality: str = "text",
        retry: int = 5,
    ):
        """
        Example method that requests a minimal function definition from the model,
        adapted to support multimodal inputs (text, image_url, image_base64, audio)
        and an optional output modality for the response.

        'df' is actually a list of dictionaries here, each dict representing one "row."
        If 'columns' is not specified, we will gather all keys found in the data.

        Parameters
        ----------
        df : List[Dict[str, Any]]
            Data sample (list of dicts) to inform the function definition.
        task : str, optional
            A brief description of the function's purpose.
        columns : List[str], optional
            Which keys from each dict to include in the user message.
            Defaults to gathering all keys present if None or empty.
        model_name : str, optional
            Which model to use (default: "gpt-4o-mini").
        column_modalities : Dict[str, str], optional
            Maps keys to one of {"text", "image_url", "image_base64", "audio"}.
            Keys not listed (or if None) default to "text".
        output_modality : str, optional
            Desired output modality: "text" (default), "audio", or "image".
        retry : int
            Number of retry attempts for generating + validating the definition.

        Returns
        -------
        GeneralSkill or None
            A skill object with the extracted function definition, or None if learning fails.
        """

        # Gather columns if none provided
        if not columns:
            columns_set = set()
            for row in df:
                columns_set.update(row.keys())
            columns = list(columns_set)

        # Construct the "system" message as a list of blocks
        system_blocks = [
            {
                "type": "text",
                "text": (
                    "You are a function definition builder. Your job is to produce a single valid JSON "
                    "object that describes the shape of the model’s output for a given task. "
                    "Here’s what you must do:\n\n"
                    "1) Output a top-level JSON object with exactly these fields:\n"
                    "   name: A short identifier for the function (string).\n"
                    "   description: A brief explanation of what the function does (string).\n"
                    "   strict: Set to true, so the output JSON must strictly match the schema.\n\n"
                    "2) The parameters field must contain:\n"
                    "   - type: 'object' (the top-level shape).\n"
                    "   - properties: a JSON object describing each output field by name.\n"
                    "   - required: an array listing the names of all required properties.\n"
                    "   - (Optional) additionalProperties: false if you wish to forbid extra keys.\n\n"
                    "3) Do not define input arguments. Only define the outputs the model must produce.\n"
                    "   (For instance, if building a sentiment-classification function, it should only list\n"
                    "    fields like 'category', possibly with an enum of [positive, negative, neutral].)\n\n"
                    "4) Do not return any other text. Only return the final JSON for the function definition.\n\n"
                    "Remember:\n"
                    " • The 'strict' field must be true.\n"
                    " • Your JSON must be well-formed and valid.\n"
                    " • Avoid including minItems, maxItems, or other constraints unless necessary.\n\n"
                    """ERROR:ParallelProcessor:Task 24 faced an unknown exception: litellm.BadRequestError: OpenAIException - Error code: 400 - {'error': {'message': "Invalid schema for function 'CategorizeReviews': In context=(), 'additionalProperties' is required to be supplied and to be false.", 'type': 'invalid_request_error', 'param': 'tools[0].function.parameters', 'code': 'invalid_function_parameters'}}"""
                    "Now, considering everything above, generate a strict JSON function definition "
                    "for the specified purpose."
                )
            }
        ]

        # Build the user message blocks
        user_blocks = []
        # Start with a text block referencing the "task"
        user_blocks.append({
            "type": "text",
            "text": f"Write exact JSON string function definition with requested keys: {task}"
        })

        # Then, gather data from df
        # We interpret each row's relevant columns via column_modalities
        for idx, row in enumerate(df):
            for col in columns:
                if col not in row:
                    continue
                raw_value = str(row[col]).strip()
                if not raw_value:
                    continue

                col_mod = column_modalities.get(col, "text") if column_modalities else "text"

                if col_mod == "text":
                    user_blocks.append({
                        "type": "text",
                        "text": f"{col} (row {idx}): {raw_value}"
                    })
                elif col_mod == "audio":
                    # Example: base64-encoded audio
                    user_blocks.append({
                        "type": "input_audio",
                        "input_audio": {
                            "data": raw_value,
                            "format": "wav"
                        }
                    })
                elif col_mod == "image_url":
                    user_blocks.append({
                        "type": "image_url",
                        "image_url": {"url": raw_value}
                    })
                elif col_mod == "image_base64":
                    # Check prefix for JPEG or PNG
                    prefix = "data:image/jpeg;base64," if raw_value.startswith("/9j") else "data:image/png;base64,"
                    user_blocks.append({
                        "type": "image_url",
                        "image_url": {"url": prefix + raw_value}
                    })
                else:
                    # Fallback => text
                    user_blocks.append({
                        "type": "text",
                        "text": f"{col} (row {idx}): {raw_value}"
                    })

        def flatten_blocks(blocks: List[Dict[str, Any]]) -> str:
            """
            Return a textual representation of content blocks for
            approximate token counting / debugging.
            """
            lines = []
            for b in blocks:
                if b["type"] == "text":
                    lines.append(b["text"])
                elif b["type"] == "image_url":
                    lines.append("[IMAGE_URL]")
                elif b["type"] == "input_audio":
                    lines.append("[AUDIO]")
                else:
                    lines.append(f"[{b['type'].upper()}]")
            return "\n".join(lines)

        system_str = flatten_blocks(system_blocks)
        user_str = flatten_blocks(user_blocks)

        system_msg = {
            "role": "system",
            "content": system_blocks,
            "content_str": system_str
        }
        user_msg = {
            "role": "user",
            "content": user_blocks,
            "content_str": user_str
        }

        def build_output_params(modality: str) -> Dict[str, Any]:
            """
            Returns top-level fields for specifying the model's output modality.
            """
            if modality == "audio":
                return {
                    "modalities": ["text", "audio"],
                    "audio": {
                        "voice": "alloy",
                        "format": "wav"
                    }
                }
            elif modality == "image":
                return {
                    "modalities": ["image"]
                }
            else:
                return {
                    "modalities": ["text"]
                }

        output_params = build_output_params(output_modality)

        request_json = {
            "model": model_name,
            "messages": [system_msg, user_msg],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "minimalFunctionDefinition",
                        "strict": False,
                        "parameters": {
                            "type": "object",
                            "required": ["function_definition"],
                            "properties": {
                                "function_definition": {
                                    "type": "string",
                                    "description": "The entire function definition as a JSON string."
                                }
                            }
                        },
                        "description": "A minimal function returning a JSON string in 'function_definition'."
                    }
                }
            ],
            "tool_choice": "required",
            "temperature": 1,
        }
        request_json.update(output_params)

        flash_logger.info("Creating a minimal function definition from the model.")

        try:
            for attempt_i in range(retry):
                # First pass: ask the model to produce the function definition
                completion = self.client.chat.completions.create(**request_json)
                function_def = self._extract_function_call_arguments(completion)

                # Second pass: attempt to validate the function we got
                try:
                    validation_request = copy(request_json)
                    validation_request["tools"] = [function_def]
                    completion = self.client.chat.completions.create(**validation_request)
                    # If this succeeds, break out of the retry loop
                    break
                except Exception:
                    flash_logger.info(f"Learning attempt {attempt_i+1} of {retry} failed, retrying...")

            # We either succeeded or ran out of tries
            skill = GeneralSkill(
                model_name=model_name,
                function_definition=function_def,
                system_prompt="Exactly populate the provided function definition",
                columns=columns
            )
            return skill

        except Exception as e:
            flash_logger.error(f"Learning failed: {e}")
            return None

    def _extract_function_call_arguments(self, completion):
        """
        Extracts JSON arguments from the model's function call output.
        If nested JSON is found, we try to parse it as well.
        """
        args_str = ""
        try:
            # The new usage might store conversation tool calls here
            args_str = completion.choices[0].message.tool_calls[0].function.arguments
            args_obj = ast.literal_eval(args_str)

            # Attempt to see if it's actually a JSON string inside 'function_definition'
            try:
                # We expect something like: { "function_definition": "{ ... }" }
                # so parse that nested string
                args_obj = json.loads(args_obj["function_definition"])
                args_obj["strict"] = True
                args_obj = {
                    "type": "function",
                    "function": args_obj
                }
            except:
                # If that fails, maybe the entire args_str is raw JSON
                try:
                    args_obj = json.loads(args_str)
                except:
                    pass
            return args_obj

        except Exception as e:
            if args_str:
                return args_str
            flash_logger.error(f"Error parsing function call arguments: {e}")
            return f"<PARSE_ERROR: {e}>"