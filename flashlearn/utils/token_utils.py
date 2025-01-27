import tiktoken
from typing import List, Dict, Any

def _count_tokens_for_messages(messages: List[Dict[str, str]], model_name: str) -> int:
    """
    Count tokens for the conversation messages using tiktoken.
    Each item in `messages` is { "role": <>, "content": <> }.
    """
    enc = tiktoken.encoding_for_model(model_name)
    text = ""
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        text += f"{role}: {content}\n"
    return len(enc.encode(text))

def _count_tokens_for_function_defs(function_defs: List[Dict[str, Any]], model_name: str) -> int:
    """
    Approximate tokens for function definitions by converting them to a string
    (str() or JSON) and encoding that.
    """
    enc = tiktoken.encoding_for_model(model_name)
    total_tokens = 0
    for f_def in function_defs:
        serialized = str(f_def)
        total_tokens += len(enc.encode(serialized))
    return total_tokens

def count_tokens_for_task(task: Dict[str, Any], default_model: str) -> int:
    """
    Given a single task dict with structure:
       {
         "custom_id": <>,
         "request": {
             "model": <modelname>,
             "messages": [...],
             "functions": [...],
             ...
         }
       }
    count the tokens from messages and function definitions.
    """
    req_data = task.get("request", {})
    model_name = req_data.get("model", default_model)
    messages = req_data.get("messages", [])
    functions = req_data.get("functions", [])

    tokens_messages = _count_tokens_for_messages(messages, model_name)
    tokens_funcs = _count_tokens_for_function_defs(functions, model_name)
    return tokens_messages + tokens_funcs

def count_tokens_for_tasks(tasks: List[Dict[str, Any]], default_model: str) -> int:
    """
    Sum token count across every task.
    """
    total = 0
    for t in tasks:
        total += count_tokens_for_task(t, default_model)
    return total