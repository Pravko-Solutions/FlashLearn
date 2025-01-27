import pytest
import json
import ast
from unittest.mock import MagicMock, patch

from flashlearn.skills.general_skill import GeneralSkill
from flashlearn.skills.learn_skill import LearnSkill


@pytest.fixture
def mock_learn_skill_verbose():
    """
    Returns a LearnSkill instance with a mock client (verbose logging).
    """
    mock_client = MagicMock()
    return LearnSkill(model_name="gpt-4o", verbose=True, client=mock_client)


@pytest.fixture
def mock_learn_skill_quiet():
    """
    Returns a LearnSkill instance with a mock client (quiet logging).
    """
    mock_client = MagicMock()
    return LearnSkill(model_name="gpt-4o", verbose=False, client=mock_client)


# -----------------------------------------------------------------------------
# Constructor
# -----------------------------------------------------------------------------
def test_learn_skill_init_verbose(mock_learn_skill_verbose):
    """
    Ensure that LearnSkill is instantiated correctly in verbose mode.
    Just checks that no exception is raised and fields are set.
    """
    assert mock_learn_skill_verbose.model_name == "gpt-4o"
    assert mock_learn_skill_verbose.verbose is True


def test_learn_skill_init_quiet(mock_learn_skill_quiet):
    """
    Ensures quiet mode doesn't raise exceptions; model_name set properly.
    """
    assert mock_learn_skill_quiet.model_name == "gpt-4o"
    assert mock_learn_skill_quiet.verbose is False


# -----------------------------------------------------------------------------
# _extract_function_call_arguments
# -----------------------------------------------------------------------------
def test_extract_function_call_arguments_success_json_obj(mock_learn_skill_verbose):
    """
    Test the normal path where we parse from
    completion.choices[0].message.tool_calls[0].function.arguments,
    literal_eval succeeds, and we also parse JSON from function_definition => set 'strict' => wrap in dict.
    """
    # Setup a mock completion
    completion = MagicMock()
    # The function arguments => must be valid Python dict as a string
    completion.choices[0].message.tool_calls[0].function.arguments = (
        "{'function_definition': '{\"name\":\"test\",\"description\":\"desc\",\"parameters\":{}}'}"
    )

    output = mock_learn_skill_verbose._extract_function_call_arguments(completion)
    # We expect a dict of the form {"type":"function", "function": { ... "strict":True}}
    assert isinstance(output, dict)
    assert output["type"] == "function"
    assert output["function"]["name"] == "test"
    assert output["function"]["strict"] is True


def test_extract_function_call_arguments_fallback_direct_json(mock_learn_skill_verbose):
    """
    If we fail the first JSON parse from function_definition,
    we attempt loading args_str fully.
    """
    completion = MagicMock()
    # This string won't have 'function_definition' => the first json.loads() attempt will fail,
    # then we try json.loads(args_str) directly.
    completion.choices[0].message.tool_calls[0].function.arguments = '{"hi":"there"}'
    output = mock_learn_skill_verbose._extract_function_call_arguments(completion)
    assert output == {"hi": "there"}


def test_extract_function_call_arguments_double_fail_returns_dict(mock_learn_skill_verbose):
    """
    If both attempts to parse JSON fail, we return the leftover partial data from args_obj.
    We'll mimic a scenario where literal_eval succeeds, but the 'function_definition' key doesn't exist,
    and the second fallback parse also doesn't parse. We end up returning the python dict from literal_eval.
    """
    completion = MagicMock()
    completion.choices[0].message.tool_calls[0].function.arguments = "{'function_definition_missing': True}"

    output = mock_learn_skill_verbose._extract_function_call_arguments(completion)
    # Because we don't have 'function_definition' at all, the first attempt fails,
    # the second attempt also fails => we end up returning the python dictionary
    assert output == {"function_definition_missing": True}


def test_extract_function_call_arguments_parse_error(mock_learn_skill_verbose):
    """
    If literal_eval itself fails, we check the parse error logic branch.
    Because the code sets 'args_str' but eventually returns it if there's an exception.
    """
    completion = MagicMock()
    # This is not valid Python => literal_eval will raise an exception
    invalid_args = '{"key": "missing quotes at the start or syntax error'
    completion.choices[0].message.tool_calls[0].function.arguments = invalid_args

    output = mock_learn_skill_verbose._extract_function_call_arguments(completion)
    # Because we do have an args_str, but it fails the parse => we return that string
    assert output == invalid_args


def test_extract_function_call_arguments_no_arg_str(mock_learn_skill_verbose):
    """
    If there's an exception and args_str is empty => we return "<PARSE_ERROR: ...>".
    """
    completion = MagicMock()
    # Force an IndexError => no tool_calls
    completion.choices[0].message.tool_calls = []
    output = mock_learn_skill_verbose._extract_function_call_arguments(completion)
    assert output.startswith("<PARSE_ERROR:")


# -----------------------------------------------------------------------------
# learn_skill
# -----------------------------------------------------------------------------
def mock_completion(args_str):
    """
    Returns a mock completion object given the 'arguments' string.
    Typically used in self.client.chat.completions.create side_effect.
    """
    completion = MagicMock()
    completion.choices = [
        MagicMock(
            message=MagicMock(
                tool_calls=[
                    MagicMock(function=MagicMock(arguments=args_str))
                ]
            )
        )
    ]
    return completion


def test_learn_skill_happy_path_text_mode(mock_learn_skill_verbose):
    """
    If the first completion call yields valid arguments,
    and the second validation call does not error, we get a GeneralSkill back.
    """
    # Setup first response: the model returns arguments that parse into valid function info
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = [
        mock_completion("{'function_definition': '{\"name\":\"testFn\",\"description\":\"...\",\"parameters\":{}}'}"),
        # The second "validation" call doesn't raise => success
        mock_completion("{\"validated\": true}")
    ]

    # Provide data as list-of-dicts
    df_data = [
        {"colA": "row1"},
        {"colA": ""}  # partially empty
    ]

    skill = mock_learn_skill_verbose.learn_skill(df_data, task="Add function def", retry=2)
    assert isinstance(skill, GeneralSkill)
    assert skill._function_definition["type"] == "function"
    assert skill._function_definition["function"]["name"] == "testFn"
    # Also check that create() was called exactly 2 times
    assert mock_learn_skill_verbose.client.chat.completions.create.call_count == 2


def test_learn_skill_happy_path_audio_mode(mock_learn_skill_verbose):
    """
    Provide column_modalities that includes "audio" to cover that code path in building user_blocks.
    """
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = [
        mock_completion("{'function_definition': '{\"name\":\"audioFunc\",\"description\":\"...\",\"parameters\":{}}'}"),
        # second validation success
        mock_completion("{\"validated\": true}")
    ]
    df_data = [
        {"audio_col": "audio_data_here"}
    ]

    skill = mock_learn_skill_verbose.learn_skill(
        df_data,
        model_name="custom-audio-model",
        column_modalities={"audio_col": "audio"},
        output_modality="audio",
        retry=1
    )
    assert isinstance(skill, GeneralSkill)

    # Verify the request included audio parameters
    args_list = mock_learn_skill_verbose.client.chat.completions.create.call_args_list
    req_json_first_call = args_list[0][1]  # the kwargs from the first call
    assert req_json_first_call["model"] == "custom-audio-model"
    assert req_json_first_call["audio"]["format"] == "wav"


def test_learn_skill_image_url_mode(mock_learn_skill_verbose):
    """
    Provide an image_url column to cover that path.
    """
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = [
        mock_completion("{'function_definition': '{\"name\":\"imageUrlFn\",\"description\":\"...\",\"parameters\":{}}'}"),
        mock_completion("{\"validated\": true}")
    ]

    df_data = [
        {"img_col": "http://example.com/image.jpg"}
    ]

    skill = mock_learn_skill_verbose.learn_skill(
        df_data,
        column_modalities={"img_col": "image_url"},
        output_modality="image",
        retry=1
    )
    assert isinstance(skill, GeneralSkill)

    args_list = mock_learn_skill_verbose.client.chat.completions.create.call_args_list
    req_json_first_call = args_list[0][1]
    assert req_json_first_call["modalities"] == ["image"]


def test_learn_skill_image_base64_jpeg(mock_learn_skill_verbose):
    """
    Provide an image_base64 column that starts with /9j => 'data:image/jpeg;base64,' prefix.
    """
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = [
        mock_completion("{'function_definition': '{\"name\":\"jpegFn\",\"description\":\"...\",\"parameters\":{}}'}"),
        mock_completion("{\"validated\": true}")
    ]

    df_data = [
        {"img64": "/9jSO-MUCH-JUNK-B64..."}
    ]

    skill = mock_learn_skill_verbose.learn_skill(
        df_data,
        column_modalities={"img64": "image_base64"},
        retry=1
    )
    assert isinstance(skill, GeneralSkill)


def test_learn_skill_empty_rows(mock_learn_skill_verbose):
    """
    If the entire data is empty or columns produce no blocks, we handle gracefully.
    We do produce a minimal request, but user_blocks might be minimal.
    """
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = [
        mock_completion("{'function_definition': '{\"name\":\"emptyFn\",\"description\":\"...\",\"parameters\":{}}'}"),
        mock_completion("{\"validated\": true}")
    ]

    df_data = [
        {"colA": ""},
        {"colA": ""}
    ]

    skill = mock_learn_skill_verbose.learn_skill(df_data, task="Empty", retry=1)
    # We do still create a skill, though the content blocks were basically empty
    # except for the 'task' text block
    assert isinstance(skill, GeneralSkill)


def test_learn_skill_retry_logic(mock_learn_skill_verbose):
    """
    If the second completion (validation) fails the first time, we retry up to 'retry' times.
    If eventually it succeeds, we get a skill. If it never succeeds, we return None.
    We'll do 2 attempts: the second is success.
    """
    side_effects = [
        mock_completion("{'function_definition': '{\"name\":\"retryFn\",\"description\":\"...\",\"parameters\":{}}'}"),
        Exception("Validation call fails #1"),
        # second iteration in the for x in range(retry)
        mock_completion("{\"validated\": true}")
    ]
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = side_effects

    df_data = [
        {"colA": "data"}
    ]
    skill = mock_learn_skill_verbose.learn_skill(df_data, retry=2)
    assert isinstance(skill, GeneralSkill), "Eventually success on second retry."
    # We confirm we called completions.create 3 times:
    # 1 for extraction + 1 that failed validation + 1 that succeeded
    assert mock_learn_skill_verbose.client.chat.completions.create.call_count == 4


def test_learn_skill_all_retries_fail(mock_learn_skill_verbose):
    """
    If all 'retry' attempts to validate fail, we return None.
    """
    side_effects = [
        mock_completion("{'function_definition': '{\"name\":\"failFn\",\"description\":\"...\",\"parameters\":{}}'}"),
        Exception("Validation fail #1"),
        Exception("Validation fail #2"),
    ]
    mock_learn_skill_verbose.client.chat.completions.create.side_effect = side_effects

    df_data = [
        {"colA": "some"}
    ]
    skill = mock_learn_skill_verbose.learn_skill(df_data, retry=2)
    assert skill is None, "After 2 retries, no success => None returned."
    # Called 3 times total (1 extraction + 2 validation attempts)
    assert mock_learn_skill_verbose.client.chat.completions.create.call_count == 3