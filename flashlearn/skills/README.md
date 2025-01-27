# FlashLearn Skill Classes Guide

## Understanding the Skill Architecture

In FlashLearn, a **Skill** is an object that encapsulates:

- The system prompt (high-level instruction for the LLM).
- A method to convert your dataset rows (dicts) into Chat Completion "tasks."
- A method to parse the model’s results into a structured outcome (usually JSON).
- A JSON function definition describing the shape of the output.

Internally, this ensures that every LLM response is valid JSON, aligned with your function schema.

All Skill classes inherit from `BaseSkill` (`flashlearn/skills/base_skill.py`). For data-centric workflows (where each row of data might contain text/image/audio), you often extend `BaseDataSkill` (`flashlearn/skills/base_data_skill.py`), which adds convenient methods to build content blocks for each row.

## Base Classes Overview

### BaseSkill (Abstract)

- Contains the main interface that all Skills share.
- Manages concurrency and organizes tasks via `run_tasks_in_parallel()`.
- Does not itself handle how to break down "rows" of data into blocks—that’s for specialized children.
- Requires two abstract methods to implement:
  - `create_tasks(self, df, **kwargs) → List[Dict[str,Any]]`
  - `_build_function_def(self) → Dict[str,Any]`

### BaseDataSkill

- Inherits from `BaseSkill`.
- Provides convenient methods to:
  - build content blocks from a dict of data.
  - flatten blocks for debug logging.
  - a default implementation of `create_tasks(...)` that assumes “one row = one request.”
  - `parse_function_call(...)` helper to decode JSON arguments from the Chat Completion’s function_call field.

Most skill classes in `flashlearn/skills/` simply override or extend `BaseDataSkill`.

## Building a Classification Skill

`ClassificationSkill` is a typical example (see `flashlearn/skills/classification.py`).

Key steps to create a custom classification skill:

1. Inherit from `BaseDataSkill`.
2. Define your custom `__init__` that sets things like `self.categories`, prompts, etc.
3. Implement `_build_function_def()` to return the JSON schema describing the classification output.
4. (Optionally) override `parse_result(...)` to extract the categories from the function output.

This structure forces the model to produce an output that matches the classification schema (e.g., `{"categories": ["positive"]}` or `{"categories": ["cat"]}`).

**Example Template:**

```python
from typing import Dict, Any, List
from flashlearn.skills.base_data_skill import BaseDataSkill

class MyClassificationSkill(BaseDataSkill):
    def __init__(
        self,
        model_name: str,
        categories: List[str],
        max_categories: int = 1,
        system_prompt: str = "",
        client=None
    ):
        super().__init__(model_name=model_name, system_prompt=system_prompt, client=client)
        self.categories = categories
        self.max_categories = max_categories

    def _build_function_def(self) -> Dict[str, Any]:
        # Return JSON schema that forces the model to output something like
        # {"categories": ["some_category_here"]}
        # If you only want a single category, you might use "type": "string"
        # or if you want multiple, "type": "array"
        if self.max_categories == 1:
            prop_def = {
                "type": "string",
                "enum": self.categories,
                "description": "One chosen category."
            }
        else:
            prop_def = {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": self.categories
                },
                "description": "List of chosen categories."
            }

        return {
            "type": "function",
            "function": {
                "name": "my_classification_function",
                "description": "Return one or more categories for the given text.",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "categories": prop_def
                    },
                    "required": ["categories"],
                    "additionalProperties": False
                }
            }
        }

    def parse_result(self, raw_result: Dict[str, Any]) -> Any:
        """
        Example of how to parse the categories from the model's JSON output.
        """
        # We can just call parse_function_call(arg_name="categories")
        # which uses the base_data_skill logic to parse the function call JSON
        categories_ret = self.parse_function_call(raw_result, arg_name="categories")
        if not categories_ret:
            return []
        if isinstance(categories_ret, str):
            return [categories_ret]
        return categories_ret
```

By default, `create_tasks(...)` from `BaseDataSkill` will handle your list-of-dicts. Any dictionary in the list is turned into a “task” with content blocks. If you need special grouping logic (e.g., group multiple rows into one request), just override `create_tasks(...)`.

## Building a Label Discovery Skill

If you’d like a “Labeling” or `DiscoverLabelsSkill`, you might want to combine multiple data rows into a single request so the model sees the entire dataset. In that case:

1. Inherit from `BaseDataSkill`.
2. Override `create_tasks(...)` to combine all data into a single user message.
3. In `_build_function_def()`, define the shape you expect for discovered labels, e.g., `{"labels": [...]}`.

See `flashlearn/skills/discover_labels.py` for a concrete example:

- Instead of “one row = one task,” it aggregates all rows into a single user message.
- The function definition expects `{ "labels": ["some_label", "another_label"] }`.

## GeneralSkill – A Flexible, Customizable Skill

Sometimes you have a JSON schema that doesn’t neatly fit classification or labeling. You can use `GeneralSkill` (`flashlearn/skills/general_skill.py`).

`GeneralSkill`:

- Inherits from `BaseDataSkill`.
- Lets you directly provide a custom JSON function definition at initialization.
- You can parse results however you like (override `parse_result`).

For example, if you have a custom function definition JSON describing how you want the model to respond, you can do:

```python
from flashlearn.skills.general_skill import GeneralSkill

my_function_def = {
  "type": "function",
  "function": {
    "name": "do_something",
    "description": "Perform a custom transformation on text data.",
    "strict": True,
    "parameters": {
      "type": "object",
      "properties": {
        "transformed_text": {"type": "string"},
      },
      "required": ["transformed_text"],
      "additionalProperties": False
    }
  }
}

skill = GeneralSkill(
    model_name="gpt-4o-mini",
    function_definition=my_function_def,
    system_prompt="Rewrite the text in a comedic style."
)
```

Then `skill.create_tasks(...)` will transform your list of dicts into tasks, and the model’s response must match the shape of `do_something`’s parameters.

## Example: Using the ClassificationSkill

Below is a more complete example demonstrating how to classify IMDB reviews into “positive” or “negative”. This sample shows you how to:

1. Set up the skill.
2. Convert your data (a list of dicts) into tasks via `create_tasks()`.
3. Run them in parallel.
4. Collect and compare results.

**Example Usage Code:**

```python
import json
import os
from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import imdb_reviews_50k

def main():
    # Step 1: Setup your provider
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'
    # or any other client config if you have your own LLM endpoint

    # Step 2: Load sample data (list of dicts with "review" and "sentiment" keys)
    reviews = imdb_reviews_50k(sample=100)

    # Step 3: Initialize the Classification Skill
    skill = ClassificationSkill(
        model_name="gpt-4o-mini",  # or "deepseek-chat", etc.
        client=OpenAI(),
        categories=["positive", "negative"],
        max_categories=1,
        system_prompt="We want to classify short movie reviews by sentiment."
    )

    # Step 4: Prepare classification tasks (only keep 'review' to classify)
    removed_sentiment = [{'review': x['review']} for x in reviews]
    tasks = skill.create_tasks(removed_sentiment)

    # Step 5: Write tasks out (optional for debug or batch usage)
    with open('tasks.jsonl', 'w') as jsonl_file:
        for entry in tasks:
            jsonl_file.write(json.dumps(entry) + '\n')

    # Step 6: Run classification tasks in parallel
    results = skill.run_tasks_in_parallel(
        tasks,
        max_requests_per_minute=1000,
        max_tokens_per_minute=1500000
    )

    # Step 7: Map results & measure accuracy
    correct = 0
    for i, review in enumerate(reviews):
        predicted_cats = results[str(i)]['categories']
        reviews[i]['predicted_category'] = predicted_cats
        if review['sentiment'] == predicted_cats:
            correct += 1
    accuracy = round(correct / len(reviews), 2)
    print(f'Accuracy: {accuracy * 100}%')

    # Save final results
    with open('results.jsonl', 'w') as jsonl_file:
            for entry in reviews:
            jsonl_file.write(json.dumps(entry) + '\n')

    # Step 8: Save the skill definition for future loading
    skill.save("BinaryClassificationSkill.json")

if __name__ == "__main__":
    main()
```

## Example: Loading a Skill Definition from the "toolkit"

If you have a pre-made skill definition in the "toolkit," you can load it via `GeneralSkill.load_skill(...)`. This loads a stored JSON definition (like `ClassifyDifficultyOfQuestion`) and uses it directly.

```python
import json
import os
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import ClassifyDifficultyOfQuestion
from flashlearn.utils import imdb_reviews_50k

def main():
    # Step 1: (Optional) Provide your LLM credentials
    # os.environ["OPENAI_API_KEY"] = "API_KEY"

    # Step 2: Load data
    reviews = imdb_reviews_50k(sample=50)

    # Step 3: Load the previously created ClassificationSkill definition
    # In this example, we have a “toolkit” definition named ClassifyDifficultyOfQuestion
    skill = GeneralSkill.load_skill(ClassifyDifficultyOfQuestion)

    # Step 4: Create tasks
    tasks = skill.create_tasks(reviews)

    # Step 5: Run tasks in parallel
    results = skill.run_tasks_in_parallel(tasks)
    print("Results:", results)

if __name__ == "__main__":
    main()
```

## Custom Create Tasks Logic

If you want to group multiple rows into a single request, or do something else (like summarizing the entire dataset in a single call), you can override `create_tasks(...)`. For example:

```python
class MyAggregatedSkill(BaseDataSkill):
    def create_tasks(
        self,
        df: List[Dict[str, Any]],
        column_modalities: Dict[str, str] = None,
        output_modality: str = "text",
        **kwargs
    ) -> List[Dict[str, Any]]:
        # Combine all rows into a single user message
        all_blocks = []
        for row in df:
            blocks = self.build_content_blocks(row, column_modalities)
            all_blocks.extend(blocks)

        # Flatten to a single string if needed
        flattened_str = self.flatten_blocks_for_debug(all_blocks)

        # Wrap into a single system message + user message
        system_msg = {
            "role": "system",
            "content": self.system_prompt,
            "content_str": self.system_prompt
        }
        user_msg = {
            "role": "user",
            "content": all_blocks,
            "content_str": flattened_str
        }

        request_body = {
            "model": self.model_name,
            "messages": [system_msg, user_msg],
            "tools": [self._build_function_def()],
            "tool_choice": "required"
        }
        request_body.update(self.build_output_params(output_modality))

        # Return a list with a single “aggregated” task
        return [{"custom_id": "0", "request": request_body}]
```

## Final Notes & Best Practices

- Always define a "strict" JSON schema in your function definition so FlashLearn can guarantee your model’s output is valid JSON with the correct fields.
- Use `parse_result(...)` to convert the raw JSON to your desired structure.
- If you have multiple steps (e.g., discover labels -> classify with those labels), just chain the results from the first skill into the second skill.

Whether you’re building a classification skill, labeling skill, topic extraction skill, or advanced summarization skill, the pattern remains consistent:

- Inherit from `BaseDataSkill` (or `BaseSkill`).
- Provide a JSON function definition in `_build_function_def()`.
- (Optionally) override `create_tasks(...)` to shape how data is batched.
- (Optionally) override `parse_result(...)` to interpret the model’s final JSON.

Happy building!
