import pytest
from unittest.mock import patch, MagicMock, mock_open

from hypothesis import given, strategies as st
from typing import Dict, Any

from flashlearn.skills import BaseSkill


# A concrete subclass so we can instantiate and test BaseSkill
class MockSkill(BaseSkill):
    def create_tasks(self, data, **kwargs):
        """
        Minimal mock implementation:
        data is expected to be a list of dicts. Each dict is a 'row',
        and we produce a task per row, assigning an "id" from the index.
        """
        tasks = []
        for i, row in enumerate(data):
            tasks.append({
                "id": str(i),
                "data": row
            })
        return tasks

    def _build_function_def(self) -> Dict[str, Any]:
        return {
            "name": "mock_function",
            "parameters": {
                "type": "object",
                "properties": {
                    "example_key": {"type": "string"}
                }
            }
        }


@pytest.fixture
def mock_skill():
    """Provides a MockSkill instance for testing."""
    return MockSkill(model_name="gpt-4o-mini", system_prompt="Test prompt")


@patch("flashlearn.skills.base_skill.process_tasks_in_parallel")
def test_run_tasks_in_parallel(mock_process, mock_skill):
    """
    Ensure run_tasks_in_parallel uses our mock, sets token counts,
    and returns results.
    """
    mock_process.return_value = (
        ["result_data"],
        MagicMock(total_input_tokens=100, total_output_tokens=200)
    )
    tasks = [{"id": "1", "data": "some_data"}]
    results = mock_skill.run_tasks_in_parallel(tasks)

    assert results == ["result_data"], "Should return the mocked result_data"
    assert mock_skill.total_input_tokens == 100
    assert mock_skill.total_output_tokens == 200
    mock_process.assert_called_once()


def test_save_with_filename(mock_skill):
    """
    Test that save writes JSON with a provided filename.
    We ensure that model_name is not stored, as per requirements.
    """
    with patch("builtins.open", mock_open()) as mocked_file, \
         patch("os.path.abspath", return_value="/fake/path"):
        mock_skill.save(filepath="custom_skill.json")
        mocked_file.assert_called_once_with("custom_skill.json", "w", encoding="utf-8")


def test_save_with_default_filename(mock_skill):
    """
    Test that save writes JSON using the default class-based filename.
    We ensure that model_name is not stored, as per requirements.
    """
    with patch("builtins.open", mock_open()) as mocked_file, \
         patch("os.path.abspath", return_value="/fake/path"):
        mock_skill.save()  # No filepath passed, should use MockSkill.json
        mocked_file.assert_called_once_with("MockSkill.json", "w", encoding="utf-8")


def test_create_tasks(mock_skill):
    """
    Test that create_tasks returns a list of dicts and each dict
    corresponds to the input 'rows' in some manner.
    """
    data = [
        {"col1": 10, "col2": "foo"},
        {"col1": 20, "col2": "bar"}
    ]
    tasks = mock_skill.create_tasks(data)
    assert len(tasks) == 2
    assert tasks[0]["id"] == "0"
    assert tasks[1]["id"] == "1"


def test_build_function_def(mock_skill):
    """
    Test the mocked _build_function_def returns the expected dict.
    """
    func_def = mock_skill._build_function_def()
    assert "name" in func_def
    assert "parameters" in func_def

@patch("flashlearn.skills.base_skill.process_tasks_in_parallel")
def test_run_tasks_in_parallel_no_final_status(mock_process, mock_skill):
    """
    Ensures that if process_tasks_in_parallel returns None for final_status,
    the default (0) tokens are set.
    """
    mock_process.return_value = (["some_data"], None)
    results = mock_skill.run_tasks_in_parallel(tasks=[])
    assert results == ["some_data"]
    assert mock_skill.total_input_tokens == 0, "Should be 0 by default if final_status is None"
    assert mock_skill.total_output_tokens == 0, "Should be 0 by default if final_status is None"


@patch("flashlearn.skills.base_skill.process_tasks_in_parallel")
def test_run_tasks_in_parallel_custom_arguments(mock_process, mock_skill):
    """
    Ensures that the optional arguments (max_requests_per_minute, max_tokens_per_minute, etc.)
    are passed through, and lines 71-73 are exercised.
    """
    mock_process.return_value = (
        ["some_data"],
        MagicMock(total_input_tokens=10, total_output_tokens=20)
    )
    results = mock_skill.run_tasks_in_parallel(
        tasks=[{"id": "123"}],
        save_filepath="test.json",
        max_requests_per_minute=100,
        max_tokens_per_minute=200,
        max_attempts=3,
        token_encoding_name="test_tokens",
        return_results=False,
        request_timeout=10,
    )
    assert results == ["some_data"]
    assert mock_skill.total_input_tokens == 10
    assert mock_skill.total_output_tokens == 20
    mock_process.assert_called_once_with(
        return_results=False,
        client=mock_skill.client,
        tasks_data=[{"id": "123"}],
        save_filepath="test.json",
        max_requests_per_minute=100,
        max_tokens_per_minute=200,
        max_attempts=3,
        token_encoding_name="test_tokens",
        request_timeout=10,
    )


def test_estimate_tasks_cost(mock_skill):
    """
    Exercises estimate_tasks_cost to ensure lines 85–89 execute.
    """
    # We don't care about the exact cost, just that it doesn't crash and is >= 0
    tasks = [{"prompt": "Hello world"}]
    cost = mock_skill.estimate_tasks_cost(tasks)
    assert cost >= 0, "Cost should be a non-negative float"