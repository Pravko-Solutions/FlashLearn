import pytest
from unittest.mock import patch, MagicMock
import litellm

from flashlearn.core import FlashLiteLLMClient


# Import your classes

def test_flash_lite_llm_client_init():
    """
    Test that we can instantiate FlashLiteLLMClient without error.
    """
    client = FlashLiteLLMClient()
    assert client is not None

def test_flash_lite_llm_client_chat_property():
    """
    Test that 'chat' property returns an object that has a 'completions' property.
    """
    client = FlashLiteLLMClient()
    # Check that client.chat is created successfully
    chat_obj = client.chat
    assert hasattr(chat_obj, "completions"), "Chat should have a 'completions' property"

def test_flash_lite_llm_client_chat_completions_property():
    """
    Test that chat.completions is an instance of Completions,
    which should have a 'create' method.
    """
    client = FlashLiteLLMClient()
    completions_obj = client.chat.completions
    assert hasattr(completions_obj, "create"), "Completions should have a 'create' method"

@patch("litellm.completion", return_value="mocked response")
def test_flash_lite_llm_client_chat_completions_create(mock_completion):
    """
    Ensure that Completions.create calls litellm.completion with the correct kwargs,
    adding {'no-log': True} automatically.
    """
    client = FlashLiteLLMClient()
    result = client.chat.completions.create(model="gpt-4", prompt="Hello Test")

    # Verify we patched litellm.completion correctly
    mock_completion.assert_called_once()
    # Extract the actual arguments passed to litellm.completion
    call_args, call_kwargs = mock_completion.call_args
    # We expect no positional args, only kwargs
    assert call_args == ()
    # Ensure 'no-log' was added and set to True
    assert call_kwargs["no-log"] is True
    # Check other expected kwargs
    assert call_kwargs["model"] == "gpt-4"
    assert call_kwargs["prompt"] == "Hello Test"

    # Finally check the mocked return value
    assert result == "mocked response"