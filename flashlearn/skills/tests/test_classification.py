import pytest
from unittest.mock import MagicMock

from flashlearn.skills import ClassificationSkill

@pytest.fixture
def single_cat_skill():
    """
    Skill configured with max_categories=1 => single category selection.
    """
    return ClassificationSkill(
        model_name="gpt-4",
        categories=["CategoryA", "CategoryB"],
        max_categories=1,
        system_prompt="Single category prompt"
    )

@pytest.fixture
def multi_cat_skill():
    """
    Skill configured with max_categories=3 => can pick up to 3 categories.
    """
    return ClassificationSkill(
        model_name="gpt-4",
        categories=["Cat1", "Cat2", "Cat3", "Cat4"],
        max_categories=3,
        system_prompt="Multi category prompt"
    )

@pytest.fixture
def unlimited_cat_skill():
    """
    Skill configured with max_categories=-1 => unlimited picks in array form.
    """
    return ClassificationSkill(
        model_name="gpt-4",
        categories=["X", "Y", "Z"],
        max_categories=-1,
        system_prompt="Unlimited category prompt"
    )

def test_instantiate_single_cat_skill(single_cat_skill):
    """
    Simple check that our single-category skill is instantiated
    with the correct fields.
    """
    assert single_cat_skill.model_name == "gpt-4"
    assert single_cat_skill.categories == ["CategoryA", "CategoryB"]
    assert single_cat_skill.max_categories == 1
    assert single_cat_skill.system_prompt == "Single category prompt"

def test_instantiate_multi_cat_skill(multi_cat_skill):
    """
    Verify multi-cat skill’s fields.
    """
    assert multi_cat_skill.model_name == "gpt-4"
    assert multi_cat_skill.categories == ["Cat1", "Cat2", "Cat3", "Cat4"]
    assert multi_cat_skill.max_categories == 3

def test_instantiate_unlimited_cat_skill(unlimited_cat_skill):
    """
    Verify unlimited-cat skill’s fields.
    """
    assert unlimited_cat_skill.max_categories == -1

def test_build_function_def_single_cat(single_cat_skill):
    """
    If max_categories=1 => the schema property is type=string with an enum of the categories.
    """
    func_def = single_cat_skill._build_function_def()
    assert func_def["type"] == "function"
    assert "function" in func_def

    fdef = func_def["function"]
    assert "parameters" in fdef

    props = fdef["parameters"]["properties"]
    assert "categories" in props

    cat_prop = props["categories"]
    assert cat_prop["type"] == "string"
    assert cat_prop["enum"] == ["CategoryA", "CategoryB"]
    # No 'maxItems' since it's a string schema

def test_build_function_def_multi_cat(multi_cat_skill):
    """
    If max_categories=3 => the schema property is an array with items=enum, and maxItems=3.
    """
    func_def = multi_cat_skill._build_function_def()
    fdef = func_def["function"]
    cat_prop = fdef["parameters"]["properties"]["categories"]

    assert cat_prop["type"] == "array"
    assert cat_prop["items"]["enum"] == ["Cat1", "Cat2", "Cat3", "Cat4"]
    assert cat_prop["maxItems"] == 3

def test_build_function_def_unlimited_cat(unlimited_cat_skill):
    """
    If max_categories=-1 => the schema property is an array with no maxItems.
    """
    func_def = unlimited_cat_skill._build_function_def()
    cat_prop = func_def["function"]["parameters"]["properties"]["categories"]

    assert cat_prop["type"] == "array"
    assert "maxItems" not in cat_prop, "Should not have maxItems if max_categories is -1."

def test_parse_result_none(single_cat_skill):
    """
    parse_function_call returns None => parse_result returns [].
    """
    single_cat_skill.parse_function_call = MagicMock(return_value=None)
    output = single_cat_skill.parse_result({})
    assert output == [], "If parse_function_call None => empty list"

def test_parse_result_single_string(single_cat_skill):
    """
    parse_function_call returns a string => parse_result wraps it in a list.
    """
    single_cat_skill.parse_function_call = MagicMock(return_value="OnlyOneCat")
    output = single_cat_skill.parse_result({})
    assert output == ["OnlyOneCat"]

def test_parse_result_list(multi_cat_skill):
    """
    parse_function_call returns a list => parse_result returns that list as-is.
    """
    multi_cat_skill.parse_function_call = MagicMock(return_value=["Cat1", "Cat3"])
    output = multi_cat_skill.parse_result({})
    assert output == ["Cat1", "Cat3"]

def test_create_tasks_inherits_behavior(multi_cat_skill):
    """
    Just verify we can call create_tasks from the base class logic and get tasks.
    ClassificationSkill doesn’t override create_tasks, so it should produce
    tasks just like the parent. We pass a list of dicts (no DataFrame).
    """
    data = [
        {"text": "Hello world"},
        {"text": ""}
    ]
    tasks = multi_cat_skill.create_tasks(data)
    # Should produce 1 task (the second dict is empty => skip).
    assert len(tasks) == 1
    assert tasks[0]["custom_id"] == "0"

    req = tasks[0]["request"]
    # Confirm the classification function definition is used
    assert req["tools"][0]["function"]["name"] == "categorize_text"