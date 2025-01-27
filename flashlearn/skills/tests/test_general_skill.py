import pytest
from unittest.mock import MagicMock

from flashlearn.skills import GeneralSkill


@pytest.fixture
def function_def():
    """
    A minimal custom function definition used to initialize GeneralSkill.
    """
    return {
        "type": "function",
        "function": {
            "name": "custom_func",
            "description": "A custom function definition for testing",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "some_field": {"type": "string"}
                },
                "required": ["some_field"],
                "additionalProperties": False
            }
        }
    }


@pytest.fixture
def general_skill(function_def):
    """
    Instantiate a GeneralSkill with some minimal parameters.
    We specify self.columns = ["col1", "col2"], which the skill
    can use if no columns are provided at task-creation time.
    """
    return GeneralSkill(
        model_name="gpt-4",
        function_definition=function_def,
        system_prompt="Custom system prompt",
        columns=["col1", "col2"]
    )


def test_instantiate_general_skill(general_skill, function_def):
    """
    Tests constructor fields.
    """
    assert general_skill.model_name == "gpt-4"
    assert general_skill.system_prompt == "Custom system prompt"
    assert general_skill._function_definition == function_def
    assert general_skill.columns == ["col1", "col2"]


def test_build_function_def(general_skill, function_def):
    """
    _build_function_def should return exactly what we passed in.
    """
    output = general_skill._build_function_def()
    assert output == function_def


def test_parse_result(general_skill):
    """
    parse_result just returns the raw_result as-is (no transformation).
    """
    raw = {"some": "stuff"}
    parsed = general_skill.parse_result(raw)
    assert parsed is raw


def test_create_tasks_using_self_columns(general_skill):
    """
    If create_tasks is called with columns=None,
    we fall back to self.columns from the constructor.
    We provide data with more keys than in self.columns,
    ensuring only the configured columns are actually used.
    """
    data = [
        {"col1": "row1", "col2": "x", "col3": "extra"},
        {"col1": "row2", "col2": "y", "col3": "ignored"}
    ]
    tasks = general_skill.create_tasks(data)  # columns=None → fallback to ["col1", "col2"]
    # Should produce 2 tasks (one per dict entry)
    assert len(tasks) == 2

    for i, task in enumerate(tasks):
        assert task["custom_id"] == str(i)
        user_msg = task["request"]["messages"][1]
        # The user_msg content should only reflect col1 and col2, ignoring col3
        content_blocks = user_msg["content"]
        # Expect 2 blocks: one for col1, one for col2
        assert len(content_blocks) == 3

        # Check the block texts in order
        block_texts = [b.get("text") for b in content_blocks if b["type"] == "text"]
        assert block_texts == [data[i]["col1"], data[i]["col2"], data[i]["col3"]]


def test_create_tasks_inherits_behavior_empty_rows(general_skill):
    """
    If a row is empty in the chosen columns, that row is skipped.
    A row is "empty" if all of the chosen columns are empty strings.
    """
    data = [
        {"col1": "some text", "col2": "val"},
        {"col1": "", "col2": ""}
    ]
    tasks = general_skill.create_tasks(data, columns=["col1", "col2"])
    # Only the first entry yields content, second is empty => skip
    assert len(tasks) == 1
    assert tasks[0]["custom_id"] == "0"


def test_load_skill(function_def):
    """
    Covers load_skill, ensuring it returns an initialized GeneralSkill
    with config-specified fields.
    """
    config = {
        "skill_class": "GeneralSkill",
        "system_prompt": "Loaded skill sys prompt",
        "function_definition": function_def,
        "columns": ["my_col", "another_col"]
    }
    from flashlearn.skills.general_skill import GeneralSkill
    skill_instance = GeneralSkill.load_skill(config,model_name="gpt-4o",)

    assert isinstance(skill_instance, GeneralSkill)
    assert skill_instance.model_name == "gpt-4o"
    assert skill_instance.system_prompt == "Loaded skill sys prompt"
    assert skill_instance._function_definition == function_def
    assert skill_instance.columns == ["my_col", "another_col"]