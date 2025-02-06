# Automated PR Reviews
## Pro tip: Ctrl + C -> ChatGPT -> Ctrl + V -> Describe your problem-> Get your code

---

## Step 0: Imports and Environment Setup

In this step, we import the necessary libraries, optionally set environment variables (like API keys), and prepare a folder for storing JSON artifacts (e.g., skills, tasks, final results).

### Environment Setup

Load your environment, import libraries, and create any folders (if necessary) for saving JSON artifacts (skills, tasks, etc.).

```python
import os
import json

# Example: If using OpenAI, set your API key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Create a folder for JSON artifacts
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Environment setup.")
```

---

## Step 1: Prepare or Generate Example Pull Request Data

Here, we create synthetic (text-based) PR data that includes code changes in a “diff_summary” field. Each entry might contain:  
• A title summarizing the PR.  
• A description of what’s changed or the intent of the PR.  
• A diff_summary showing actual code modifications (in Markdown fenced code blocks).

### Prepare Example PR Data

We define a list of dictionaries, each representing a single pull request with:
- A PR title
- A descriptive overview
- Code changes in a "diff_summary" field

```python
# Example Pull Request data with code changes
pull_requests = [
    {
        "title": "Fix NullPointerException in user service",
        "description": "Addresses a null reference issue in user_service.py by properly initializing the user object.",
        "diff_summary": """```python
- user = get_current_user()
+ user = get_current_user() or User()
```"""
    },
    {
        "title": "Refactor database config handling",
        "description": "Consolidates repeated DB logic into a single function, improving maintainability.",
        "diff_summary": """```python
- def connect_db(user, password, dbname):
-     # repeated logic
-     connection = create_connection(user, password, dbname)
+ def connect_db(credentials):
+     # consolidated logic
+     connection = create_connection(
+         credentials.username,
+         credentials.password,
+         credentials.dbname
+     )
```"""
    },
    {
        "title": "Add basic error handling to payment flow",
        "description": "Wraps payment process in try-except and logs errors for debugging.",
        "diff_summary": """```python
- def process_payment(amount, card):
-     success = gateway.authorize(amount, card)
-     return success
+ import logging

+ def process_payment(amount, card):
+     try:
+         success = gateway.authorize(amount, card)
+         return success
+     except GatewayError as e:
+         logging.error(f"Payment failed: {str(e)}")
+         return False
```"""
    }
]

print("Step 1 complete: Example PR data prepared.")
print("Sample PR entry:", pull_requests[0])
```

---

## Step 2: Define the Skill for Automated PR Review

We will create a skill (e.g., using flashlearn) that analyzes each PR for potential issues, style changes, or best practices. Here, we define a “ReviewSkill” that generates recommended actions or comments based on each PR’s data.

### Define an AI “ReviewSkill”

We simulate a skill that inspects each PR’s text fields (title, description, diff_summary) and returns structured feedback, such as a concise summary and a list of action items.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill

def create_review_skill():
    learner = LearnSkill(
        model_name="gpt-4o-mini",  # Example model name
        verbose=True
    )
    
    # Example instruction for how to review
    review_instruction = (
        "You are an AI code reviewer. For each PR, please read the title, "
        "description, and diff_summary, then return JSON with the following keys:\n"
        "- 'summary': a concise summary of potential issues or improvements\n"
        "- 'action_items': a short list (array) of recommended improvements or checks\n"
        "Focus on code quality, style, and potential errors, referencing the code changes if possible."
    )
    
    # We learn the skill with a small sample of our PR data or placeholders
    skill = learner.learn_skill(
        pull_requests,
        task=review_instruction,
        model_name="gpt-4o-mini"
    )
    
    return skill

review_skill = create_review_skill()
print("Step 2 complete: 'ReviewSkill' defined and created.")
```

---

## Step 3: Store the Learned Review Skill as JSON

We save the newly learned skill (which includes prompts, model settings, etc.) in JSON. This prevents us from reconstructing it every time.

### Store the Learned Skill in JSON

We serialize the skill for future re-use.

```python
review_skill_path = os.path.join(json_folder, "pr_review_skill.json")
review_skill.save(review_skill_path)
print(f"Step 3 complete: Skill saved to {review_skill_path}")
```

---

## Step 4: Load the Saved Review Skill

To perform PR reviews at any time, we load the skill from the JSON file instead of re-learning.

### Load the Saved Skill

Restore the skill from JSON for immediate usage.

```python
from flashlearn.skills import GeneralSkill

loaded_review_skill = GeneralSkill.load_skill(review_skill_path)
print("Step 4 complete: Skill loaded from JSON:", loaded_review_skill)
```

---

## Step 5: Create Review Tasks

We convert each pull request record into a format (“tasks”) that the skill knows how to process. Since all the data is text-based (title, description, diff_summary), we specify their modalities as text.

### Create Tasks for Review

In this step, we transform each PR entry into a “task” the AI skill can interpret appropriately.

```python
column_modalities = {
    "title": "text",
    "description": "text",
    "diff_summary": "text"
}

review_tasks = loaded_review_skill.create_tasks(
    pull_requests,
    column_modalities=column_modalities
)

print("Step 5 complete: Review tasks created.")
print("Sample review task:", review_tasks[0])
```

---

## Step 6: (Optional) Save Review Tasks to JSONL

We can store tasks in a JSONL file to facilitate offline processing, auditing, or re-use.

### Save Review Tasks to JSONL (Optional)

This step ensures reproducibility and a clear record of how tasks were prepared.

```python
review_tasks_path = os.path.join(json_folder, "pr_review_tasks.jsonl")
with open(review_tasks_path, 'w') as f:
    for task in review_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Step 6 complete: Review tasks saved to {review_tasks_path}")
```

---

## Step 7: Load Review Tasks from JSONL (Optional)

We demonstrate how to reload the tasks from JSONL, if needed in a separate environment.

### Load Review Tasks from JSONL (Optional)

Shows how tasks can be reloaded before running them, enabling offline or separate environment workflows.

```python
loaded_review_tasks = []
with open(review_tasks_path, 'r') as f:
    for line in f:
        loaded_review_tasks.append(json.loads(line))

print("Step 7 complete: Review tasks reloaded.")
print("Example reloaded task:", loaded_review_tasks[0])
```

---

## Step 8: Run the Automated Review

We now pass these tasks to the loaded skill. The AI reviews each PR’s text (including code changes) and returns a JSON output with a “summary” and “action_items.”

### Run the Automated PR Review

We run the tasks in parallel (or sequentially) and retrieve structured feedback from the AI on each PR.

```python
review_results = loaded_review_skill.run_tasks_in_parallel(loaded_review_tasks)

print("Step 8 complete: PR reviews finished.")
print("Sample result (task_id, review):")
for task_id, review_data in list(review_results.items())[:1]:
    print(f"  Task ID {task_id}: {review_data}")
```

---

## Step 9: Map the Review Output Back to the Pull Requests

We typically want each PR to have the AI’s feedback attached, so we can display or further act on it. By mapping each task’s result to its original record, we get an integrated data structure.

### Integrate Review Output into Original Data

We attach each review result to the corresponding PR, preserving the association between code changes and recommended actions.

```python
annotated_prs = []
for task_id_str, output_json in review_results.items():
    task_id = int(task_id_str)
    pr_record = pull_requests[task_id]
    pr_record["review"] = output_json
    annotated_prs.append(pr_record)

print("Step 9 complete: Mapped review output back to PR data.")
print("Sample annotated PR:", annotated_prs[0])
```

---

## Step 10: Store the Annotated Results

Finally, we can store the AI-reviewed PRs in a JSONL file (or another format). This makes it easy to integrate into dashboards, continuous integration systems, or further analysis pipelines.

### Store the PR Review Results

We write the annotated PRs to a JSONL file, preserving both the original data and the AI’s commentary.

```python
final_reviews_path = os.path.join(json_folder, "pr_review_results.jsonl")
with open(final_reviews_path, 'w') as f:
    for pr in annotated_prs:
        f.write(json.dumps(pr) + '\n')

print(f"Step 10 complete: Final AI review results saved to {final_reviews_path}")
```

---

## Summary and Next Steps

Using this tutorial, you can automate PR reviews by:

1. Gathering pull request data (title, descriptions, code diffs).  
2. Training or configuring a skill to analyze that data and produce actionable feedback (summary and action items).  
3. Storing and loading skill definitions and tasks in JSON/JSONL, ensuring reproducibility and offline/parallel usage.  
4. Mapping results back into your PR system for developers and stakeholders.

You can further extend this approach by:  
- Enriching prompts or examples for domain-specific code styles (e.g., Python best practices, security checks).  
- Providing more advanced code snippets or scanning large diffs.  
- Using a second skill to automatically create or update JIRA tickets or Slack notifications based on the review output.  
