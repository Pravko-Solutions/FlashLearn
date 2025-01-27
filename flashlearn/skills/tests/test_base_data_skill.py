import pytest
from flashlearn.skills.base_data_skill import BaseDataSkill

class TestBaseDataSkill:
    """
    A concrete test suite for BaseDataSkill ensuring coverage
    of all methods under the new dict-based API.
    """

    @pytest.fixture
    def skill(self):
        """
        Provide an instance of BaseDataSkill with minimal arguments.
        """
        return BaseDataSkill(model_name="gpt-4", system_prompt="Test prompt")

    # --------------------------------------------------------------------------
    # build_output_params
    # --------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "modality, expected",
        [
            (
                "audio",
                {
                    "modalities": ["text", "audio"],
                    "audio": {"voice": "alloy", "format": "wav"}
                },
            ),
            ("image", {"modalities": ["image"]}),
            ("text", {"modalities": ["text"]}),
            ("unknown", {"modalities": ["text"]}),
        ]
    )
    def test_build_output_params(self, skill, modality, expected):
        """
        Ensure build_output_params covers all branches (audio, image, text, fallback).
        """
        result = skill.build_output_params(modality)
        assert result == expected

    # --------------------------------------------------------------------------
    # build_content_blocks
    # --------------------------------------------------------------------------
    def test_build_content_blocks_text(self, skill):
        """
        If the column modality is "text", we add a text block.
        """
        row = {"col1": "hello"}
        blocks = skill.build_content_blocks(row, {"col1": "text"})
        assert len(blocks) == 1
        assert blocks[0]["type"] == "text"
        assert blocks[0]["text"] == "hello"

    def test_build_content_blocks_missing_column(self, skill):
        """
        If column_modalities references a key not in row, we simply won't see it
        since build_content_blocks loops over row's keys.
        There's no error raised.
        """
        row = {"col1": "hello"}
        # "not_in_df" won't appear because it's not in row
        blocks = skill.build_content_blocks(row, {"not_in_df": "text"})
        # We only process "col1"
        assert len(blocks) == 1
        assert blocks[0]["type"] == "text"
        assert blocks[0]["text"] == "hello"

    def test_build_content_blocks_empty_value(self, skill):
        """
        Rows with empty string => skip those blocks.
        """
        row = {"col1": ""}
        blocks = skill.build_content_blocks(row, {"col1": "text"})
        assert len(blocks) == 0

    def test_build_content_blocks_audio(self, skill):
        """
        If modality is audio, produce input_audio block with 'data' and 'format'.
        """
        row = {"audio_col": "some_audio_data"}
        blocks = skill.build_content_blocks(row, {"audio_col": "audio"})
        assert len(blocks) == 1
        assert blocks[0]["type"] == "input_audio"
        assert blocks[0]["input_audio"]["data"] == "some_audio_data"
        assert blocks[0]["input_audio"]["format"] == "wav"

    def test_build_content_blocks_image_url(self, skill):
        """
        If modality is image_url, produce an 'image_url' block with a 'url'.
        """
        row = {"img_col": "http://example.com/image.jpg"}
        blocks = skill.build_content_blocks(row, {"img_col": "image_url"})
        assert len(blocks) == 1
        assert blocks[0]["type"] == "image_url"
        assert blocks[0]["image_url"]["url"] == "http://example.com/image.jpg"

    def test_build_content_blocks_image_base64_jpeg(self, skill):
        """
        If modality is image_base64, check that we prepend 'data:image/jpeg;base64,'
        if the string starts with '/9j'.
        """
        row = {"img64_col": "/9jBASE64STRING"}
        blocks = skill.build_content_blocks(row, {"img64_col": "image_base64"})
        assert len(blocks) == 1
        assert blocks[0]["type"] == "image_url"
        assert blocks[0]["image_url"]["url"].startswith("data:image/jpeg;base64,/9jBASE64STRING")

    def test_build_content_blocks_image_base64_png(self, skill):
        """
        If modality is image_base64, check that we prepend 'data:image/png;base64,'
        if it doesn't start with '/9j'.
        """
        row = {"img64_col": "iVBORw0KGgoAAAANSUhEUg"}
        blocks = skill.build_content_blocks(row, {"img64_col": "image_base64"})
        assert len(blocks) == 1
        assert blocks[0]["type"] == "image_url"
        assert blocks[0]["image_url"]["url"].startswith("data:image/png;base64,")

    def test_build_content_blocks_fallback_modality(self, skill):
        """
        If modality is unknown, fallback to 'text'.
        """
        row = {"colX": "some text"}
        blocks = skill.build_content_blocks(row, {"colX": "something_else"})
        assert len(blocks) == 1
        assert blocks[0]["type"] == "text"
        assert blocks[0]["text"] == "some text"

    # --------------------------------------------------------------------------
    # flatten_blocks_for_debug
    # --------------------------------------------------------------------------
    def test_flatten_blocks_for_debug(self, skill):
        """
        Test each recognized block type to ensure the correct bracketed placeholders
        or text are returned.
        """
        blocks = [
            {"type": "text", "text": "Hello world"},
            {"type": "image_url", "image_url": {"url": "http://example.com"}},
            {"type": "input_audio", "input_audio": {"data": "audio_data", "format": "wav"}},
            {"type": "custom_type"},
        ]
        result = skill.flatten_blocks_for_debug(blocks)
        lines = result.split("\n")
        assert lines[0] == "Hello world"
        assert lines[1] == "[IMAGE_URL]"
        assert lines[2] == "[AUDIO]"
        assert lines[3] == "[CUSTOM_TYPE]"

    # --------------------------------------------------------------------------
    # create_tasks
    # --------------------------------------------------------------------------
    def test_create_tasks_default(self, skill):
        """
        Verify that create_tasks produces one task per dict,
        skipping any that produce no content blocks.
        By default, output_modality="text".
        """
        data = [
            {"col1": "hello"},
            {"col1": ""}
        ]
        tasks = skill.create_tasks(data)  # no special column_modalities
        # First dict has data => 1 task, second dict is blank => no content => skip
        assert len(tasks) == 1

        task = tasks[0]
        assert task["custom_id"] == "0"

        request = task["request"]
        # Should have 'model', 'messages', 'tools', 'tool_choice'
        assert "model" in request
        assert "messages" in request
        assert "tools" in request
        assert request["tool_choice"] == "required"
        # Should have default "modalities" = ["text"]
        assert request["modalities"] == ["text"]

    def test_create_tasks_with_custom_modality_columns(self, skill):
        """
        Provide column_modalities + output_modality="audio" to test coverage.
        """
        data = [
            {
                "txt_col": "Hello text.",
                "aud_col": "my-audio-data",
                "empty_col": ""
            }
        ]
        tasks = skill.create_tasks(
            data,
            column_modalities={"txt_col": "text", "aud_col": "audio", "empty_col": "text"},
            output_modality="audio",
            columns=["txt_col", "aud_col", "empty_col"],  # ignored by method, but allowed
        )
        assert len(tasks) == 1
        task = tasks[0]
        assert task["custom_id"] == "0"

        request = task["request"]
        assert "messages" in request
        # from output_params for "audio"
        assert "audio" in request

        # user_msg is the second item in messages
        user_block = request["messages"][1]["content"]
        # we expect 2 blocks: text + audio (the empty_col was skipped)
        assert len(user_block) == 2
        text_block = user_block[0]
        audio_block = user_block[1]
        assert text_block["type"] == "text"
        assert audio_block["type"] == "input_audio"

    # --------------------------------------------------------------------------
    # parse_result
    # --------------------------------------------------------------------------
    def test_parse_result_returns_raw(self, skill):
        """
        parse_result simply returns the raw_result as-is by default.
        """
        raw = {"some": "thing"}
        output = skill.parse_result(raw)
        assert output is raw

    # --------------------------------------------------------------------------
    # parse_function_call
    # --------------------------------------------------------------------------
    def test_parse_function_call_success(self, skill):
        """
        Test a valid function_call with arguments => ensure we parse it properly.
        """
        raw = {
            "choices": [
                {
                    "message": {
                        "function_call": {
                            "arguments": '{"categories": ["catA", "catB"]}'
                        }
                    }
                }
            ]
        }
        parsed = skill.parse_function_call(raw, arg_name="categories")
        assert parsed == ["catA", "catB"]

    def test_parse_function_call_no_function_call_key(self, skill):
        """
        Missing 'function_call' in the message => returns None.
        """
        raw = {
            "choices": [
                {
                    "message": {
                        # no function_call key
                    }
                }
            ]
        }
        parsed = skill.parse_function_call(raw)
        assert parsed is None

    def test_parse_function_call_empty_args(self, skill):
        """
        If 'arguments' is missing or empty => None.
        """
        raw = {
            "choices": [
                {
                    "message": {
                        "function_call": {
                            # no arguments
                        }
                    }
                }
            ]
        }
        parsed = skill.parse_function_call(raw)
        assert parsed is None

    def test_parse_function_call_exception(self, skill):
        """
        If we can't parse the arguments JSON => we catch and return None.
        """
        raw = {
            "choices": [
                {
                    "message": {
                        "function_call": {
                            "arguments": "this is invalid JSON"
                        }
                    }
                }
            ]
        }
        parsed = skill.parse_function_call(raw)
        assert parsed is None

    # --------------------------------------------------------------------------
    # _build_function_def
    # --------------------------------------------------------------------------
    def test_build_function_def(self, skill):
        """
        Ensure the default function definition is a valid structure
        containing required keys.
        """
        func_def = skill._build_function_def()
        assert "type" in func_def
        assert func_def["type"] == "function"
        assert "function" in func_def
        assert "parameters" in func_def["function"]
        assert "strict" in func_def["function"]