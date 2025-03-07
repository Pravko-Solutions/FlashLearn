# Automated Financial Data Extraction
---
In this guide, we’ll walk through setting up an AI-driven workflow that reads a company’s yearly financial report and turns it into structured data. From building and saving a custom extraction skill to mapping the AI outputs back to your original documents, we’ll cover each step to get you from raw text to meaningful numbers.

## Step 0: Imports and Environment Setup

First, we import our necessary libraries, set any environment variables (e.g., API keys), and create a folder to store JSON artifacts (e.g., skills, tasks, final results).

### Environment Setup

We import libraries, optionally define credentials, and create a directory to store JSON artifacts that keep our workflow reproducible.

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

## Step 1: Prepare Financial Text Excerpts

We create synthetic text excerpts that resemble sections from a yearly financial report. Each excerpt might contain references to gross profit, EBITDA, net income, or other metrics. You can expand or replace these with real data as needed.

### Prepare or Generate Yearly Report Data

We define a list of text entries mimicking sections of a company's yearly financial report. Each entry is a short paragraph referencing various financial metrics.

```python
financial_texts = [
    {
        "report_section": (
            "In 2022, the company reported a gross profit of $1.2B, an EBITDA of $900M, "
            "and a net income of $500M. Operating expenses increased slightly compared to 2021."
        )
    },
    {
        "report_section": (
            "For the fiscal year 2023, gross profit grew to $1.5B, while net income reached $650M. "
            "EBITDA was reported at approximately $1.1B. The company also introduced new products."
        )
    },
    {
        "report_section": (
            "Our consolidated statement shows that total revenue surpassed $3B, with a gross profit "
            "of $1.8B, and EBITDA climbed to $1.2B. Net income remained around $700M this year."
        )
    }
]

print("Step 1 complete: Financial text data prepared.")
print("Sample text entry:", financial_texts[0])
```

---

## Step 2: Define an AI Skill for Financial Data Extraction

We’ll use flashlearn’s approach to create a skill that extracts structured data points like gross profit, EBITDA, and net income from each text record.

### Define a “FinancialExtractionSkill”

We instruct the AI to parse each text for specific metrics (gross profit, EBITDA, net income) and return these as structured JSON. In a real scenario, you can add more or adjust them as needed.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill

def create_financial_extraction_skill():
    learner = LearnSkill(
        model_name="gpt-4o-mini",  # Example model name
        verbose=True
    )
    
    # Instruction/prompt outline:
    extraction_instruction = (
        "You are an AI system that extracts financial metrics. For each report_section, "
        "please return a JSON with keys: 'gross_profit', 'ebitda', 'net_income'. "
        "Provide values as floats in millions. If a metric is missing, set it to a default (e.g., 0)."
    )
    
    skill = learner.learn_skill(
        df=[], # You could pass examples if you do not get desired accuracy
        task=extraction_instruction,
        model_name="gpt-4o-mini"
    )
    
    return skill

financial_skill = create_financial_extraction_skill()
print("Step 2 complete: Financial extraction skill defined and created.")
```

---

## Step 3: Store the Learned Skill as JSON

We can serialize the newly learned skill (which includes prompts, model configurations, etc.) into a JSON file for reproducibility or reuse in other environments.

### Store the Learned Skill

This ensures we don’t need to re-learn the skill each time, preserving the instructions and settings.

```python
financial_skill_path = os.path.join(json_folder, "financial_extraction_skill.json")
financial_skill.save(financial_skill_path)
print(f"Step 3 complete: Skill saved to {financial_skill_path}")
```

---

## Step 4: Load the Saved Skill

We can load the skill whenever we want to run the extraction without re-learning.

### Load the Saved Skill

We demonstrate how to restore the skill from the JSON file.

```python
financial_skill_path = os.path.join(json_folder, "financial_extraction_skill.json")
with open(financial_skill_path, "r", encoding="utf-8") as file:
    definition = json.load(file)
loaded_financial_skill = GeneralSkill.load_skill(definition)
print("Step 4 complete: Skill loaded from JSON:", loaded_financial_skill)
```

---

## Step 5: Create Extraction Tasks

We now create tasks from each text snippet, letting the skill know which columns to read as text. Because our data has “report_section” fields, we’ll map that field to text.

### Create Tasks for Extraction

We transform each excerpt into a task that the AI skill can process. In this case, “report_section” is categorized as text.

```python
column_modalities = {
    "report_section": "text"
}

extraction_tasks = loaded_financial_skill.create_tasks(
    financial_texts,
    column_modalities=column_modalities
)

print("Step 5 complete: Extraction tasks created.")
print("Sample extraction task:", extraction_tasks[0])
```

---

## Step 6: (Optional) Save Extraction Tasks to JSONL

It’s often helpful to store tasks in JSONL format so you can process them offline or in a separate environment.

### Save Extraction Tasks to JSONL (Optional)

Storing the tasks ensures an auditable chain of how each record is processed.

```python
extraction_tasks_path = os.path.join(json_folder, "financial_extraction_tasks.jsonl")
with open(extraction_tasks_path, 'w') as f:
    for task in extraction_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Step 6 complete: Extraction tasks saved to {extraction_tasks_path}")
```

---

## Step 7: Load Extraction Tasks from JSONL (Optional)

If desired, load the tasks again from JSONL—useful when you’re running them in a new session or environment.

### Load Extraction Tasks from JSONL (Optional)

This demonstrates how to recreate the tasks from the stored JSONL file.

```python
loaded_extraction_tasks = []
with open(extraction_tasks_path, 'r') as f:
    for line in f:
        loaded_extraction_tasks.append(json.loads(line))

print("Step 7 complete: Extraction tasks reloaded.")
print("Sample reloaded task:", loaded_extraction_tasks[0])
```

---

## Step 8: Run the Financial Data Extraction

We run the tasks through the loaded skill. The AI extracts numerical values for the specified metrics from each text snippet.

### Execute Data Extraction

We run the tasks in parallel (or sequentially), obtaining structured financial metrics for each text record.

```python
extraction_results = loaded_financial_skill.run_tasks_in_parallel(loaded_extraction_tasks)

print("Step 8 complete: Data extraction finished.")
print("Sample result (task_id, output):")
for task_id, extracted_data in list(extraction_results.items())[:1]:
    print(f"  Task ID {task_id}: {extracted_data}")
```

---

## Step 9: Map the Extraction Output Back to the Original Data

We attach each extraction output (the structured metrics) to its corresponding text entry, producing a final annotated dataset.

### Integrate Extraction Results with Original Data

We map each result by task ID, preserving the link between source text and extracted metrics.

```python
annotated_financials = []
for task_id_str, output_json in extraction_results.items():
    task_id = int(task_id_str)
    record = financial_texts[task_id]
    record["extracted_metrics"] = output_json
    annotated_financials.append(record)

print("Step 9 complete: Mapped extraction output to financial data.")
print("Annotated record example:", annotated_financials[0])
```

---

## Step 10: Store the Final Annotated Results

Finally, we can store our annotated financial data in a JSONL file for further analysis, integration with trading algorithms, or additional forecasting.

### Save the Annotated Financial Data

We write the updated records (including extracted metrics) to a JSONL file, ready for automated reporting or integration with downstream applications.

```python
final_extraction_path = os.path.join(json_folder, "financial_extraction_results.jsonl")
with open(final_extraction_path, 'w') as f:
    for entry in annotated_financials:
        f.write(json.dumps(entry) + '\n')

print(f"Step 10 complete: Final extracted data saved to {final_extraction_path}")
```

---

## Summary and Next Steps

Using these steps, you can:

- Generate or load textual representations of a yearly financial report.  
- Train (or configure) an AI skill to identify and extract specific metrics like gross profit, EBITDA, net income, and so on.  
- Store all tasks and skill definitions in JSON or JSONL for auditable, reproducible workflows.  
- Integrate the extracted data with automated trading or forecasting systems, or produce structured financial reporting for stakeholders.

Next steps might include:

- Expanding the set of financial metrics you parse.  
- Combining extraction with summarization tasks to produce automated commentary for each report.  

This completes our example for using AI to extract structured financial data (gross profit, EBITDA, net income, etc.) from yearly report text!
