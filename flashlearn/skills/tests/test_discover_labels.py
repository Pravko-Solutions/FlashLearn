import pytest
from unittest.mock import MagicMock

from flashlearn.skills import DiscoverLabelsSkill

@pytest.fixture
def discover_skill_limited():
    """
    DiscoverLabelsSkill with label_count=3 (i.e., user can select up to 3 labels).
    """
    return DiscoverLabelsSkill(
        model_name="gpt-4",
        label_count=3,
        system_prompt="Label the dataset please."
    )

@pytest.fixture
def discover_skill_unlimited():
    """
    DiscoverLabelsSkill with label_count=-1 => no limit.
    """
    return DiscoverLabelsSkill(
        model_name="gpt-4",
        label_count=-1,
        system_prompt="Unlimited labeling."
    )

def test_instantiate_discover_skill(discover_skill_limited):
    """
    Verify basic instantiation fields.
    """
    assert discover_skill_limited.model_name == "gpt-4"
    assert discover_skill_limited.label_count == 3
    assert discover_skill_limited.system_prompt == "Label the dataset please."

def test_create_tasks_limited(discover_skill_limited):
    """
    create_tasks should aggregate all rows into one request.
    label_count=3 => system prompt includes 'You may select up to 3 labels.'
    """
    data = [
        {"col1": "data 1"},
        {"col1": "data 2"}
    ]
    tasks = discover_skill_limited.create_tasks(data)
    assert len(tasks) == 1, "Should produce exactly one task."

    task = tasks[0]
    assert task["custom_id"] == "0"

    req = task["request"]
    assert req["model"] == "gpt-4"
    # Tools => function def named 'infer_labels'
    assert req["tools"][0]["function"]["name"] == "infer_labels"

    # System prompt appended with label_count
    assert "up to 3 labels" in req["messages"][0]["content"]

    # User message should combine the 2 row-blocks
    user_content = req["messages"][1]["content"]
    # We expect 2 text blocks since both rows had content
    assert len(user_content) == 2

def test_create_tasks_unlimited(discover_skill_unlimited):
    """
    label_count=-1 => system prompt includes 'You may select any number of labels.'
    """
    data = [
        {"col1": "rowA"},
        {"col1": "rowB"},
        {"col1": "rowC"}
    ]
    tasks = discover_skill_unlimited.create_tasks(data)
    assert len(tasks) == 1

    req = tasks[0]["request"]
    assert "any number of labels" in req["messages"][0]["content"]

def test_create_tasks_empty_df(discover_skill_limited):
    """
    If no blocks are created (all empty?), return [].
    """
    data = [
        {"col1": ""},
        {"col1": ""}
    ]
    tasks = discover_skill_limited.create_tasks(data)
    assert tasks == [], "No content => no tasks generated."

def test_build_function_def(discover_skill_limited):
    """
    Ensure the function definition is structured as expected (top-level 'type'
    and 'function', with parameters => type=array).
    """
    func_def = discover_skill_limited._build_function_def()
    assert func_def["type"] == "function"

    f_def = func_def["function"]
    assert f_def["name"] == "infer_labels"
    assert "parameters" in f_def

    props = f_def["parameters"]["properties"]
    assert "labels" in props

    labels_prop = props["labels"]
    assert labels_prop["type"] == "array"
    assert labels_prop["items"]["type"] == "string"

def test_parse_result_none(discover_skill_limited):
    """
    parse_function_call returns None => parse_result => [].
    """
    discover_skill_limited.parse_function_call = MagicMock(return_value=None)
    result = discover_skill_limited.parse_result({})
    assert result == [], "If parse_function_call is None => empty list"

def test_parse_result_list(discover_skill_limited):
    """
    parse_function_call returns a list => parse_result returns the list as-is.
    """
    discover_skill_limited.parse_function_call = MagicMock(return_value=["label1", "label2"])
    result = discover_skill_limited.parse_result({})
    assert result == ["label1", "label2"]