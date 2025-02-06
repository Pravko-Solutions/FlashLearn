# Improve Customer Segmentation
## Pro tip: Ctrl + C -> ChatGPT -> Ctrl + V -> Describe your problem-> Get your code
---

## Step 0: Imports and Environment Setup

In this step, we import the necessary libraries, optionally set environment variables (like API keys), and prepare a folder for storing JSON artifacts (e.g., skills, tasks, final segmentation results).

### Environment Setup

Import libraries, set up any credentials, and prepare folders for saving JSON artifacts.

```python
import os
import json

# (Optional) If using OpenAI or another provider:
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Create a folder for JSON artifacts
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Environment setup.")
```

---

## Step 1: Prepare or Generate Synthetic Customer Data

Here, we'll create some synthetic customer data. Each record might represent a customer’s engagement and purchase patterns. For illustration, each record can have:  
- A unique customer ID  
- Average monthly spend  
- Number of monthly purchases  
- Whether or not they use premium features  
- A textual summary or note

### Prepare Synthetic Customer Data

We define a list of dictionaries representing each customer’s key metrics.

```python
import random

def generate_synthetic_customers(num_customers=10):
    data = []
    for i in range(num_customers):
        monthly_spend = round(random.uniform(20, 200), 2)
        purchases = random.randint(0, 15)
        uses_premium = random.choice([True, False])
        notes = "High engagement" if purchases > 10 else "Moderate engagement"
        
        data.append({
            "customer_id": f"CUST_{i:03d}",
            "monthly_spend": monthly_spend,
            "monthly_purchases": purchases,
            "uses_premium": uses_premium,
            "notes": notes
        })
    return data

customer_data = generate_synthetic_customers(12)

print("Step 1 complete: Synthetic customer data generated.")
print("Sample customer record:", customer_data[0])
```

---

## Step 2: Define an AI Skill for Segmentation

We will use flashlearn to create or learn a skill that segments customers into a fixed set of categories (e.g., “High-value,” “At-risk,” “Occasional,” etc.), or returns a new suggested segmentation based on patterns observed in the data. In a real scenario, you might refine instructions, add domain knowledge, or provide explicit examples.

### Define a Segmentation Skill

We simulate a skill that reads each customer’s data and outputs a segmented category, plus a brief rationale.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill

def create_segmentation_skill():
    learner = LearnSkill(
        model_name="gpt-4o-mini",  # Example model name
        verbose=True
    )
    
    # Example instruction for segmentation
    segmentation_instruction = (
        "You are an AI system that analyzes customer data for segmentation. Describe also data ranges in description for given dataset "
        "For each record, consider monthly_spend, monthly_purchases, uses_premium, and notes. "
        "Return JSON with the following keys:\n"
        "- 'segment': the recommended segment (e.g., 'High-value,' 'Occasional,' 'At-risk,' etc.)\n"
        "- 'rationale': brief explanation of why the user fits that segment."
    )
    
    skill = learner.learn_skill(
        customer_data,
        task=segmentation_instruction,
        model_name="gpt-4o-mini"
    )
    
    return skill

segmentation_skill = create_segmentation_skill()
print("Step 2 complete: Segmentation skill defined and created.")
```

---

## Step 3: Store the Learned Skill as JSON

We save the newly created segmentation skill—including its model parameters and prompt instructions—in JSON for re-use.

### Store the Learned Skill in JSON

This preserves the skill definition so it can be loaded without re-learning.

```python
segmentation_skill_path = os.path.join(json_folder, "customer_segmentation_skill.json")
segmentation_skill.save(segmentation_skill_path)
print(f"Step 3 complete: Skill saved to {segmentation_skill_path}")
```

---

## Step 4: Load the Saved Skill

To actually perform segmentation in the future, we can load the skill from the JSON file, bypassing the need to re-learn.

### Load the Saved Skill

We restore the skill from JSON for use in processing data.

```python
loaded_segmentation_skill = GeneralSkill.load_skill(segmentation_skill_path)
print("Step 4 complete: Skill loaded from JSON:", loaded_segmentation_skill)
```

---

## Step 5: Create Segmentation Tasks

We transform each customer record into a “task” the skill can process. Generally, each record includes numerical or boolean fields, plus textual notes. We inform the skill which fields to consider as “text” if needed.

### Create Tasks for Segmentation

We convert the customer data into tasks for the segmentation skill. 

```python
# For demonstration, treat 'notes' as text; the rest remain numeric/boolean.
column_modalities = {
    "notes": "text"
}

tasks_segment = loaded_segmentation_skill.create_tasks(
    customer_data,
    column_modalities=column_modalities
)

print("Step 5 complete: Segmentation tasks created.")
print("Sample segmentation task:", tasks_segment[0])
```

---

## Step 6: (Optional) Save Segmentation Tasks to JSONL

We can store these tasks in a JSONL file for offline or separate environment processing.

### Save Segmentation Tasks to JSONL (Optional)

This helps maintain a record of task creation for reproducible workflows.

```python
tasks_segment_jsonl_path = os.path.join(json_folder, "segmentation_tasks.jsonl")
with open(tasks_segment_jsonl_path, 'w') as f:
    for task in tasks_segment:
        f.write(json.dumps(task) + '\n')

print(f"Step 6 complete: Segmentation tasks saved to {tasks_segment_jsonl_path}")
```

---

## Step 7: Load Segmentation Tasks from JSONL (Optional)

If needed, load tasks again from JSONL. This is useful when tasks are generated in one environment and processed in another.

### Load Segmentation Tasks from JSONL (Optional)

Shows how to retrieve tasks from the JSONL file so they can be processed.

```python
loaded_segmentation_tasks = []
with open(tasks_segment_jsonl_path, 'r') as f:
    for line in f:
        loaded_segmentation_tasks.append(json.loads(line))

print("Step 7 complete: Segmentation tasks reloaded from JSONL.")
print("Example loaded segmentation task:", loaded_segmentation_tasks[0])
```

---

## Step 8: Run the Segmentation

We now pass the segmentation tasks to our loaded skill. The AI produces a category and a rationale for each customer.

### Run Segmentation

We execute the tasks in parallel (or sequentially) to receive the recommended customer segment and rationale.

```python
segmentation_results = loaded_segmentation_skill.run_tasks_in_parallel(loaded_segmentation_tasks)

print("Step 8 complete: Segmentation finished.")
print("Sample result (task_id, output):")
for task_id, seg_data in list(segmentation_results.items())[:1]:
    print(f"  Task ID {task_id}: {seg_data}")
```

---

## Step 9: Map the Segmentation Output Back to the Customer Data

We attach each output (segment, rationale) back onto the corresponding customer record, facilitating analysis or additional business logic.

### Integrate Segmentation Results into Original Data

We match each task’s result to the corresponding customer record to produce a final annotated dataset.

```python
annotated_customers = []
for task_id_str, output_json in segmentation_results.items():
    task_id = int(task_id_str)
    record = customer_data[task_id]
    record["segmentation"] = output_json
    annotated_customers.append(record)

print("Step 9 complete: Mapped segmentation output to customer data.")
print("Sample annotated customer:", annotated_customers[0])
```

---

## Step 10: Store the Final Annotated Results

Finally, we write these annotated customer records (including the newly assigned segments) to a JSONL or other file for consumption by other systems, dashboards, or additional modeling.

### Store the Segmented Customer Data

We save the annotated customer records to a JSONL file for future use or integration with other pipelines.

```python
final_segments_path = os.path.join(json_folder, "customer_segmentation_results.jsonl")
with open(final_segments_path, 'w') as f:
    for cust in annotated_customers:
        f.write(json.dumps(cust) + '\n')

print(f"Step 10 complete: Final customer segmentation results saved to {final_segments_path}")
```

---

## Summary and Next Steps

This tutorial demonstrates a straightforward approach to AI-driven customer segmentation:

1. We generated synthetic customer data reflecting monthly spend, purchase frequency, and a textual “notes” column.  
2. We trained or configured a skill to segment customers into categories, also providing a rationale.  
3. We stored and loaded the skill in JSON, created tasks, saved those tasks in JSONL, and loaded them again if needed.  
4. We captured the final annotated data (segments and rationales) in a JSONL file.  

You can extend or refine this approach by:  
- Providing more detailed prompts or examples in the skill training step to handle complex real-world behaviors.  
- Incorporating numerical thresholds or advanced logic for certain segments.  
- Building subsequent tasks (e.g., marketing campaigns or personalized offers) using the assigned segments.  

This completes our guide for using AI to improve customer segmentation!
