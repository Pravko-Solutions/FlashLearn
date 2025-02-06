Certainly! Below is the content transformed into Markdown format.

# Jupyter Notebook Tutorial: Building an AI-Powered User Behavior Workflow

## Introduction

In this tutorial, we'll build an end-to-end AI workflow that:
1. Analyzes user behavior (e.g., detecting churn risk, identifying power users).
2. Automates task management based on insights (e.g., assigning tasks or follow-ups).
3. Generates clear, actionable insights for business or application decisions.

We will:
- Generate synthetic data about user interactions.
- Learn a "Skill" (using the flashlearn approach).
- Store, load, and run tasks.
- Finally, map and store the results for further analysis or automation.

This ensures reproducibility and easy sharing or re-use of the AI logic.

```python
# Step 0: Imports and Environment Setup

import os
import json
import random
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill

# (Optional) If you have OpenAI or other providers requiring an API key:
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY_HERE"

# Directory to store JSON artifacts (skills, tasks, results)
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Environment setup complete.")
```

## Step 1: Synthetic User Behavior Data

First, we'll create some synthetic data that captures user interactions. This data might represent daily usage statistics, clicks, purchases, or anything relevant to your scenario. In our example, each user will have:
- a unique user ID  
- a daily usage frequency  
- a “churn risk factor” (a random score simulating likelihood of inactivity)  
- an activity log or textual summary  

We'll produce 50 synthetic records in a simple Python list where each element is a dictionary.

```python
# Step 1: Generate Synthetic User Behavior Data

def generate_synthetic_user_data(num_records=50):
    data = []
    for i in range(num_records):
        usage = random.randint(0, 100)
        churn_risk = random.uniform(0, 1)  # 0 to 1, higher means more at-risk
        data.append({
            "user_id": f"user_{i}",
            "daily_usage": usage,
            "churn_risk_score": round(churn_risk, 2),
            "activity_summary": (
                "User frequently checks notifications, " if usage > 50 else "User occasionally logs in, "
            ) + f"churn risk {churn_risk:.2f}"
        })
    return data

# Create and inspect a small sample
user_data = generate_synthetic_user_data(num_records=50)
print(json.dumps(user_data[:3], indent=2))
```

## Step 2: Learn a Skill for Analyzing User Behavior

We will use the flashlearn "LearnSkill" approach to create a skill that classifies users into different segments (e.g., "high risk", "moderate risk", "low risk", "power user", etc.). The instructions for the skill will ask the model to do two things:  
1. Classify the user into one of a few categories based on their daily usage and churn risk.  
2. Provide a short textual insight or recommendation.

This is just an example: in a real scenario, you can refine the prompt or instructions to best match your data and goals.

```python
# Step 2: Learn the Skill

learner = LearnSkill(
    model_name="gpt-4o-mini",  # Example model name
    verbose=True
)

analysis_instruction = (
    "Given a user's daily_usage and churn_risk_score, "
    "assign a 'user_segment' under the keys: high_risk, moderate_risk, low_risk, or power_user. "
    "Additionally, provide a short insight under the key 'recommendation'. "
    "Output JSON with exactly these keys: user_segment, recommendation."
)

learned_skill = learner.learn_skill(
    user_data,
    task=analysis_instruction,
    model_name="gpt-4o-mini"  # Use the same or different model
)

print("Skill learned.")
```

## Step 3: Store the Learned Skill as JSON

Once the skill is learned, we can serialize its definition to a JSON file so we can reuse it without re-learning. This is beneficial for offline, production pipelines, or sharing with your team.

```python
# Step 3: Store the Learned Skill

skill_path = os.path.join(json_folder, "user_behavior_analysis_skill.json")
learned_skill.save(skill_path)
print(f"Skill saved to {skill_path}")
```

## Step 4: Load the Skill from JSON

To demonstrate reusability, let's load the skill from the JSON file we just saved. Flashlearn provides a simple load_skill() method on GeneralSkill.

```python
# Step 4: Load the Skill

loaded_skill = GeneralSkill.load_skill(skill_path)
print("Skill loaded from JSON:", loaded_skill)
```

## Step 5: Create Tasks

We now transform each item in our user_data list into a JSON-based "task" that can be processed by our loaded skill. These tasks often contain the user data and a minimal set of instructions or context.

```python
# Step 5: Create Tasks

tasks = loaded_skill.create_tasks(user_data)
print("Sample Task:", json.dumps(tasks[0], indent=2))
```

## Step 6: Save Tasks as JSONL

We can store these tasks in a JSONL file so that we can inspect or process them offline, or in a different environment (for example, on a machine without direct access to raw data).

```python
# Step 6: Save tasks to a JSONL file

tasks_jsonl_path = os.path.join(json_folder, "user_behavior_tasks.jsonl")
with open(tasks_jsonl_path, 'w') as f:
    for task in tasks:
        f.write(json.dumps(task) + '\n')

print(f"Tasks saved to {tasks_jsonl_path}")
```

## Step 7: Load Tasks from JSONL

When you are ready to process the tasks (e.g., in a separate workflow or after verification), reload them from JSONL.

```python
# Step 7: Load tasks from the tasks JSONL file

loaded_tasks = []
with open(tasks_jsonl_path, 'r') as f:
    for line in f:
        loaded_tasks.append(json.loads(line))

print(f"Loaded {len(loaded_tasks)} tasks from {tasks_jsonl_path}")
print("Example loaded task:", loaded_tasks[0])
```

## Step 8: Process Tasks (Analysis)

Next, we'll use our skill to process the tasks. The skill will classify users based on their data and provide a short recommendation.

```python
# Step 8: Run the tasks to generate results

analysis_results = loaded_skill.run_tasks_in_parallel(loaded_tasks)
print("Sample result (task_id, output):", list(analysis_results.items())[0])
```

## Step 9: Map the Results to Original Data

We then attach each output (by task ID) back to the corresponding user record in our dataset. This merges the model's insights with the original data, enabling easy analysis or further automation.

```python
# Step 9: Mapping results back to user_data

merged_data = []
for task_id_str, output_json in analysis_results.items():
    task_id = int(task_id_str)  # Convert string ID back to integer
    user_record = user_data[task_id]
    user_record["analysis_result"] = output_json  # e.g. {user_segment, recommendation}
    merged_data.append(user_record)

# Preview the merged data
print(json.dumps(merged_data[:2], indent=2))
```

## Step 10: Store the Final Results for Future Use

Finally, we can store the annotated user data in a JSONL file for further analytics or feeding into other processes (like automated messaging, dashboard updates, or advanced personalization).

```python
# Step 10: Store the final annotated results

final_results_path = os.path.join(json_folder, "user_behavior_analysis_results.jsonl")
with open(final_results_path, 'w') as f:
    for entry in merged_data:
        f.write(json.dumps(entry) + '\n')

print(f"Final analysis results stored at {final_results_path}")
```

# Next Steps: Automate Task Management & Generate Actionable Insights

Now that user segments and recommendations are attached to each record, we can further automate task management. For instance:

- Automatically assign a "Retention Task" for users labeled `"high_risk"`.
- Send "Thank you" messages or next-level features to `"power_user"` segments.
- Re-engage with `"moderate_risk"` or `"low_risk"` users via marketing campaigns.

In future steps, you could:
1. Create a second skill that takes these analyses and decides internal tasks to be assigned to your team (e.g., "contact user to see if they need assistance").  
2. Store and load that skill in the same manner (JSON-based).  
3. Generate a new set of tasks for an internal Task Management system (e.g., tickets, follow-ups).  
4. Run them, gather results, and feed them back into your overall system or CRM.

This tutorial demonstrates the modular nature of AI-driven workflows: each skill can be learned, stored, loaded, and run on your data pipeline, with concise JSON artifacts to ensure maintainability and reproducibility.