from abc import ABC
from typing import List, Dict, Any
import ast

from .base_skill import BaseSkill


class BaseDataSkill(BaseSkill, ABC):
    """
    Extends the plain BaseSkill with convenient methods for:
      • Building request blocks (system/user) from a list of dictionaries
        (where each dict is treated as one "row").
      • Converting key-value pairs into text/image/audio blocks using
        column_modalities to decide how each field is processed.
      • (Optionally) flattening the blocks for debugging or token usage.
      • Merging an output_modality parameter (text/audio/image).

    NOTE: We no longer use pandas.DataFrame or 'columns'; instead, we take a list of
    dictionaries (df). Each dict's keys are “columns.” The column_modalities dict
    still indicates how each key should be processed (default "text").
    """

    def build_output_params(self, modality: str) -> Dict[str, Any]:
        """
        Return extra top-level fields for the Chat Completions call:
          - 'modalities': [...]
          - If audio → specify 'audio' config
          - If image → specify 'image' config
          - Otherwise default to text
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

    def build_content_blocks(
            self,
            row: Dict[str, Any],
            column_modalities: Dict[str, str] = None
    ) -> List[Dict[str, Any]]:
        """
        Given one “row” (a dict), produce a list of content blocks:
          - { "type": "text",      "text": ... }
          - { "type": "image_url", "image_url": {"url": ...} }
          - { "type": "input_audio", "input_audio": { "data": ..., "format": ... } }

        Falls back to 'text' if modality is missing or invalid.
        """
        if column_modalities is None:
            column_modalities = {}
        content_blocks = []

        for key, val in row.items():
            raw_value = str(val).strip()
            if not raw_value:
                continue

            modality = column_modalities.get(key, "text")

            if modality == "text":
                content_blocks.append({"type": "text", "text": raw_value})

            elif modality == "audio":
                content_blocks.append({
                    "type": "input_audio",
                    "input_audio": {
                        "data": raw_value,
                        "format": "wav"
                    }
                })

            elif modality == "image_url":
                content_blocks.append({
                    "type": "image_url",
                    "image_url": {"url": raw_value}
                })

            elif modality == "image_base64":
                # Simple heuristic for JPEG vs PNG base64 prefix
                prefix = "data:image/jpeg;base64," if raw_value.startswith("/9j") else "data:image/png;base64,"
                content_blocks.append({
                    "type": "image_url",
                    "image_url": {"url": prefix + raw_value}
                })

            else:
                # Fallback: treat as text
                content_blocks.append({"type": "text", "text": raw_value})

        return content_blocks

    def flatten_blocks_for_debug(self, blocks: List[Dict[str, Any]]) -> str:
        """
        Returns a textual representation of content blocks—useful
        for debugging or approximate token counting logic.
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

    def create_tasks(
            self,
            df: List[Dict[str, Any]],
            column_modalities: Dict[str, str] = None,
            output_modality: str = "text",
            **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Default implementation: one dictionary = one task. If needed,
        child classes can override for alternative grouping strategies.

        :param df: A list of dicts; each dict is treated as a 'row'.
        :param column_modalities: Mapping from key → "text"/"image_url"/"audio"/etc.
        :param output_modality: "text", "audio", or "image"
        :param columns: (Unused) Only present for signature consistency with the original.
        :param kwargs: Additional keyword arguments, if any.
        :return: A list of tasks (each task a dict with {custom_id, request}).
        """
        if column_modalities is None:
            column_modalities = {}
        output_params = self.build_output_params(output_modality)

        tasks = []
        for idx, row in enumerate(df):
            content_blocks = self.build_content_blocks(row, column_modalities)
            if not content_blocks:
                continue

            user_text_for_prompt = self.flatten_blocks_for_debug(content_blocks)

            system_msg = {
                "role": "system",
                "content": self.system_prompt,
                "content_str": self.system_prompt
            }
            user_msg = {
                "role": "user",
                "content": content_blocks,
                "content_str": user_text_for_prompt
            }

            request_body = {
                "model": self.model_name,
                "messages": [system_msg, user_msg],
                "tools": [self._build_function_def()],
                "tool_choice": "required"
            }
            request_body.update(output_params)

            tasks.append({
                "custom_id": str(idx),
                "request": request_body
            })

        return tasks

    def parse_result(self, raw_result: Dict[str, Any]) -> Any:
        """
        By default, just return the raw result as-is.
        Child classes often override with more nuanced parsing.
        """
        return raw_result

    def parse_function_call(self, raw_result: Dict[str, Any], arg_name="categories") -> Any:
        """
        Helper to parse a function call argument from “raw_result”.

        Example: looks for a top-level 'function_call' under 'choices[0]["message"]',
        then tries to parse JSON from 'arguments', returning the key specified
        by arg_name (e.g., "categories").
        """
        try:
            message = raw_result["choices"][0]["message"]
            if "function_call" not in message:
                return None
            args_str = message["function_call"].get("arguments", "")
            if not args_str:
                return None
            args_obj = ast.literal_eval(args_str)
            return args_obj.get(arg_name, None)
        except Exception:
            return None

    def _build_function_def(self) -> Dict[str, Any]:
        """
        Minimal default function definition.
        Child classes may override with more specialized JSON schemas.
        """
        return {
            "type": "function",
            "function": {
                "name": "basic_function",
                "description": "A simple function call placeholder.",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "string"
                        }
                    },
                    "required": ["result"],
                    "additionalProperties": False
                }
            }
        }