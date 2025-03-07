
# Classifying Customer Service Requests
## Pro tip: Ctrl + C -> ChatGPT -> Ctrl + V -> Describe your problem-> Get your code
---

## Step 0: Imports and Environment Setup

We start by importing the necessary libraries, setting any environment variables (e.g., API keys), and optionally creating a folder for storing JSON artifacts (skills, tasks, results).

### Environment Setup

In this step, we import libraries, set up any credentials, and prepare folders for saving JSON artifacts.

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

## Step 1: Prepare or Create Customer Service Request Data

We create a list of dictionaries, each representing a customer service request. In a real scenario, you might have these requests in a ticketing system. Here, each request has a “message” field containing the user’s query or complaint.

### Prepare Sample Customer Service Requests

We define a list of dictionaries representing different kinds of requests. For simplicity, each has a “message” field, though you can include other metadata (ticket ID, customer ID, etc.).

```python
service_requests = [
    {"message": "I can't log into my account, please help!"},
    {"message": "My order never arrived, I want a refund."},
    {"message": "Where can I find instructions for setting up the device?"},
    {"message": "I was charged twice for the same product."},
    {"message": "How do I reset my password?"},
    {"message": "The product is damaged and I want an exchange."}
]

print("Step 1 complete: Sample data prepared.")
print("Sample service request:", service_requests[0])
```

---

## Step 2: Define or Choose a Predefined Set of Categories

We now specify the categories into which we want to classify service requests. For instance:  
• Account Issues  
• Shipping / Delivery Issues  
• Billing / Payment Issues  
• Product Support / Setup  
• Returns / Refunds  

You can tailor these categories to match your actual customer support process.

### Define Predefined Categories

We create a list of categories that we’ll use to classify each request.

```python
predefined_categories = [
    "Account Issues",
    "Shipping / Delivery Issues",
    "Billing / Payment Issues",
    "Product Support / Setup",
    "Returns / Refunds"
]

print("Step 2 complete: Predefined categories specified.")
print("Categories:", predefined_categories)
```

---

## Step 3: Create or Configure a Classification Skill

We will use flashlearn to create a “ClassificationSkill” specifying our predefined categories. This ensures each request is assigned to one or more relevant categories.

### Define a Classification Skill

We create a ClassificationSkill and provide it with our predefined categories. In a real setting, you could also include a custom prompt or instructions to help the model make decisions.

```python
from flashlearn.skills.classification import ClassificationSkill
from openai import OpenAI

def create_classification_skill(categories):
    # Create a client (OpenAI, for instance)
    client = OpenAI()

    classify_skill = ClassificationSkill(
        model_name="gpt-4o-mini",  # Example model name
        client=client,
        categories=categories
    )
    return classify_skill

classification_skill = create_classification_skill(predefined_categories)
print("Step 3 complete: Classification skill created.")
```

---

## Step 4: Save the Classification Skill as JSON (Optional)

We can store the classification skill definition in JSON, so we don’t need to recreate it every time.

### Store the Classification Skill (Optional)

This preserves the skill’s definition in a JSON file, enabling re-loading as needed.

```python
skill_path = os.path.join(json_folder, "customer_service_classification_skill.json")
classification_skill.save(skill_path)
print(f"Step 4 complete: Skill saved to {skill_path}")
```

---

## Step 5: Load the Classification Skill

When we want to classify data, we simply load the skill from JSON rather than rebuilding it. This is optional if you just created the skill in the same session.

### Load the Saved Skill

We restore the skill from JSON for immediate usage.

```python
from flashlearn.skills import GeneralSkill
skill_path = os.path.join(json_folder, "customer_service_classification_skill.json")
with open(skill_path, "r", encoding="utf-8") as file:
    definition = json.load(file)
loaded_classification_skill = GeneralSkill.load_skill(definition)
print("Step 5 complete: Skill loaded from JSON:", loaded_classification_skill)
```

---

## Step 6: Create Classification Tasks

We transform each service request into a “task” that the skill can process. Because this is text data, we can specify the “message” field as having a text modality.

### Create Tasks for Classification

We show the skill which fields it should treat as text. Here, “message” is our primary text field.

```python
column_modalities = {
    "message": "text"
}

classification_tasks = loaded_classification_skill.create_tasks(
    service_requests,
    column_modalities=column_modalities
)

print("Step 6 complete: Classification tasks created.")
print("Sample classification task:", classification_tasks[0])
```

---

## Step 7: (Optional) Save Classification Tasks to JSONL

If needed, store the tasks in a JSONL file for offline processing or reproducibility.

### Save Classification Tasks (Optional)

We store tasks to JSONL for auditing or offline usage.

```python
classification_tasks_path = os.path.join(json_folder, "service_requests_tasks.jsonl")
with open(classification_tasks_path, 'w') as f:
    for task in classification_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Step 7 complete: Classification tasks saved to {classification_tasks_path}")
```

---

## Step 8: Load Classification Tasks from JSONL (Optional)

You can reload the tasks later in a different environment, if desired.

### Load Classification Tasks from JSONL (Optional)

Demonstrates how to retrieve tasks from a JSONL file for classification.

```python
loaded_classification_tasks = []
with open(classification_tasks_path, 'r') as f:
    for line in f:
        loaded_classification_tasks.append(json.loads(line))

print("Step 8 complete: Classification tasks reloaded.")
print("Example reloaded task:", loaded_classification_tasks[0])
```

---

## Step 9: Run the Classification

We now run the classification tasks through the loaded skill. The AI model assigns each request to one or more predefined categories.

### Classify the Service Requests

We execute the tasks in parallel (or sequentially) and observe the category assignments for each request.

```python
classification_results = loaded_classification_skill.run_tasks_in_parallel(loaded_classification_tasks)

print("Step 9 complete: Classification finished.")
print("Sample result (task_id, output):")
for task_id, cat_data in list(classification_results.items())[:1]:
    print(f"  Task ID {task_id}: {cat_data}")
```

---

## Step 10: Map the Classification Results Back to the Original Data

We attach each classification result to the corresponding service request object. This way, every request now has a “classification” field that indicates the assigned category or categories.

### Integrate Classification Output into Original Requests

We match each result to the appropriate service request for a final, annotated dataset.

```python
annotated_requests = []
for task_id_str, output_json in classification_results.items():
    task_id = int(task_id_str)
    service_request = service_requests[task_id]
    service_request["classification"] = output_json
    annotated_requests.append(service_request)

print("Step 10 complete: Mapped classification output to requests.")
print("Sample annotated request:", annotated_requests[0])
```

---

## Step 11: Store the Final Classified Requests (Optional)

We can store the final labeled data in a JSONL file or other format for integration with helpdesk systems, further analysis, or dashboards.

### Store the Final Labeled Requests (Optional)

Finally, we save the annotated service requests to a JSONL file, ensuring we can ingest them into a CRM, BI tools, or analytics pipeline.

```python
final_requests_path = os.path.join(json_folder, "service_requests_classified.jsonl")
with open(final_requests_path, 'w') as f:
    for req in annotated_requests:
        f.write(json.dumps(req) + '\n')

print(f"Step 11 complete: Labeled customer service requests saved to {final_requests_path}")
```

---

## Summary and Next Steps

In this tutorial, we:

1. Created a set of typical customer service requests (text-based).  
2. Specified a list of predefined categories (e.g., Account Issues, Shipping Issues, Billing, Product Support, Returns).  
3. Built a ClassificationSkill to map each request to the relevant category or categories.  
4. Stored tasks and results in JSON/JSONL for reproducibility.  
5. Mapped classification results back to the original requests for integrated data.

You can extend this approach by incorporating more sophisticated prompts, additional categories, or advanced logic (e.g., multi-label classification, confidence scores). This completes our guide for classifying customer service requests into predefined categories!
