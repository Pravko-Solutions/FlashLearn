# Discovering Themes in Product Reviews

---

## Step 0: Imports and Environment Setup

Create or open a new Jupyter Notebook. Start by importing the necessary libraries, setting up any environment variables (e.g., API keys), and optionally creating a folder for storing JSON artifacts.

### Environment Setup

In this step, we import libraries, set any needed environment variables, and optionally create a folder for JSON artifacts (e.g., skills, tasks, results).

```python
import os
import json
from openai import OpenAI
from flashlearn.skills.discover_labels import DiscoverLabelsSkill
from flashlearn.skills.classification import ClassificationSkill

# (Optional) Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# (Optional) Create a folder for JSON artifacts
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Imports and environment setup.")
```

---

## Step 1: Prepare or Generate Text Data

We define a simple list of dictionaries with text-based reviews. Each entry has a "comment" field for demonstration purposes.

### Prepare Text Data

In this step, we compose a list of text reviews or sentences to demonstrate label discovery and classification.

```python
# Example text reviews
text_reviews = [
    {"comment": "Battery life exceeded expectations, though camera was mediocre."},
    {"comment": "Arrived late, but customer service was supportive."},
    {"comment": "The product is overpriced. I want a refund."},
    {"comment": "Fantastic design and smooth performance."},
    {"comment": "Shipping was incredibly fast, but packaging could be improved."}
]

print("Step 1 complete: Data prepared.")
print("Sample data:", text_reviews)
```

---

## Step 2: Initialize and Define the Label Discovery Skill

Label discovery is useful for automatically inferring potential categories or topics from the entire dataset.

### Define the Label Discovery Skill

Here, we use the “DiscoverLabelsSkill” to find relevant labels from the dataset in a single pass. We supply a model name and an OpenAI client.

```python
def get_discover_skill():
    # Create a client (OpenAI in this example)
    client = OpenAI()

    discover_skill = DiscoverLabelsSkill(
        model_name="gpt-4o-mini",
        client=client
    )
    return discover_skill

discover_skill = get_discover_skill()
print("Step 2 complete: Label discovery skill initialized.")
```

---

## Step 3: Create Label Discovery Tasks

We transform our list of text reviews into the “tasks” format expected by DiscoverLabelsSkill. Since this is text-only data, our column modalities can either be omitted or simply mark “comment” as text.

### Create Discovery Tasks

We convert the text data into tasks that the discovery skill can process. For text-only fields, we pass “comment” as having a “text” modality.

```python
column_modalities = {
    "comment": "text"
}

# Create discovery tasks
tasks_discover = discover_skill.create_tasks(
    text_reviews,
    column_modalities=column_modalities
)

print("Step 3 complete: Discovery tasks created.")
print("Sample discovery task:", tasks_discover[0])
```

---

## Step 4: (Optional) Save Discovery Tasks to JSONL

Although optional, saving tasks to JSONL allows for offline processing or auditing.

### Save Discovery Tasks to JSONL (Optional)

This helps maintain reproducibility and a clear record of how tasks were generated.

```python
tasks_discover_jsonl_path = os.path.join(json_folder, "discovery_tasks.jsonl")
with open(tasks_discover_jsonl_path, 'w') as f:
    for task in tasks_discover:
        f.write(json.dumps(task) + '\n')

print(f"Step 4 complete: Discovery tasks saved to {tasks_discover_jsonl_path}")
```

---

## Step 5: Load Discovery Tasks from JSONL (Optional)

You can reload the tasks from JSONL at any time. This is helpful if you are performing the discovery in a separate environment.

### Load Discovery Tasks from JSONL (Optional)

Demonstrates how to retrieve tasks from the JSONL file we just saved.

```python
loaded_discovery_tasks = []
with open(tasks_discover_jsonl_path, 'r') as f:
    for line in f:
        loaded_discovery_tasks.append(json.loads(line))

print("Step 5 complete: Discovery tasks reloaded from JSONL.")
print("A sample reloaded discovery task:", loaded_discovery_tasks[0])
```

---

## Step 6: Run Label Discovery

We now run these tasks through the discovery skill, which should suggest a set of labels or topics.

### Run Label Discovery

We request the skill to analyze all tasks, returning any discovered labels. Typically, the output is contained in a single record (often keyed by "0") with a "labels" field.

```python
discovery_output = discover_skill.run_tasks_in_parallel(loaded_discovery_tasks)
discovered_labels = discovery_output.get("0", {}).get("labels", [])

print("Step 6 complete: Labels discovered.")
print("Discovered labels:", discovered_labels)
```

---

## Step 7: Define the Classification Skill using Discovered Labels

Once we have a set of labels, we can assign them to individual data entries using ClassificationSkill.

### Classification Skill with Discovered Labels

We initialize a “ClassificationSkill” using the discovered labels, which the skill will then apply to new or existing text records.

```python
def get_classification_skill(labels):
    client = OpenAI()
    classify_skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        client=client,
        categories=labels
    )
    return classify_skill

classify_skill = get_classification_skill(discovered_labels)
print("Step 7 complete: Classification skill initialized with discovered labels.")
```

---

## Step 8: Create Classification Tasks

We now form classification tasks for each text review, letting the skill know where to find the textual content.

### Create Tasks for Classification

Here, we transform our text data into classification tasks, telling the skill which column to treat as text.

```python
tasks_classify = classify_skill.create_tasks(
    text_reviews,
    column_modalities={"comment": "text"}
)

print("Step 8 complete: Classification tasks created.")
print("Sample classification task:", tasks_classify[0])
```

---

## Step 9: Run the Classification

Next, we pass the classification tasks to the skill, retrieving a dictionary keyed by task IDs with the assigned category or categories.

### Classification

We run the tasks in parallel (if supported) or sequentially, then inspect the classification results.

```python
classification_results = classify_skill.run_tasks_in_parallel(tasks_classify)

print("Step 9 complete: Classification finished.")
print("Classification results (first few):")
for task_id, cats in list(classification_results.items())[:3]:
    print(f"  Task ID {task_id}: {cats}")
```

---

## Step 10: Map & Store the Final Labeled Data

Finally, we attach each classification result to the original text data, storing the outcome in a JSONL file for future analysis.

### Map and Store Results

We map each classification result to its corresponding data record and (optionally) write the annotated data to a JSONL file for safe-keeping and further analysis.

```python
# Map the classification results back to the original data
annotated_data = []
for task_id_str, output_json in classification_results.items():
    task_id = int(task_id_str)
    record = text_reviews[task_id]
    record["classification"] = output_json  # attach the classification result
    annotated_data.append(record)

# Print a sample annotated record
print("Sample annotated record:", annotated_data[0])

# (Optional) Save annotated data to JSONL
final_results_path = os.path.join(json_folder, "classification_results.jsonl")
with open(final_results_path, 'w') as f:
    for rec in annotated_data:
        f.write(json.dumps(rec) + '\n')

print(f"Step 10 complete: Annotated results saved to {final_results_path}")
```

---

## Summary and Next Steps

Using these steps, you have:

- Text data prepared in a list of dictionaries.  
- A label discovery skill that aggregates topics across your dataset.  
- A classification skill that assigns those discovered labels to each record.  
- Task creation, storability (JSONL), and reloadability to maintain transparent, reproducible workflows.  
- Final annotated data, also in JSONL, for deeper analytics or integration with other systems.

From here, you can refine or expand:

- Use more complex instructions for label discovery.  
- Develop additional skills (e.g., sentiment analysis, summarization).  
- Integrate discovered/classified labels into your data pipeline or dashboards.

This completes our text-only guide for discovering and classifying labels using flashlearn!