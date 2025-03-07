# Generating Personalized Emails for Accounting AI Agent


Need to send targeted emails that highlight how an AI can streamline accounting tasks? In this guide, we’ll walk through creating a personalized email generator that references each lead’s company, role, interests, and last contact.

---

## Step 0: Imports and Environment Setup

We begin by importing the necessary libraries, setting environment variables (e.g., API keys), and creating a folder to store JSON artifacts (skills, tasks, final outputs).

### Environment Setup

We import libraries, set our API keys (if needed), and ensure we have a folder for storing artifacts (skills, tasks, JSONL results).

```python
import os
import json

# (Optional) If you're using OpenAI or another provider:
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Folder to store JSON artifacts
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Environment setup.")
```

---

## Step 1: Prepare Example User/Lead Data

Each record in our dataset represents a prospective client or lead. We include fields such as their name, company, role, interest area, and a short mention of how we last contacted them. This will be used to generate personalized emails pitching our “vertical AI agent for Accounting.”

### Prepare Example Data

We define a small dataset of prospects that might be interested in our AI accounting tool. Each record includes relevant fields the AI will use to customize the email content.

```python
import random
from datetime import datetime, timedelta

def generate_fake_leads(num_leads=5):
    roles = ["Finance Manager", "Chief Accountant", "Accounting Clerk", "CFO"]
    interests = ["Tax Compliance", "Bookkeeping Automation", "Auditing Support", "Invoice Management"]
    
    data = []
    base_date = datetime.now()
    
    for i in range(num_leads):
        # Synthetic name and company
        name = f"LeadName_{i}"
        company = f"Company_{i}"
        
        # Random role, interest, and last_contact
        role = random.choice(roles)
        interest = random.choice(interests)
        days_ago = random.randint(1, 30)
        last_contact_date = (base_date - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        data.append({
            "name": name,
            "company": company,
            "role": role,
            "interest_topic": interest,
            "last_contact_date": last_contact_date
        })
    
    return data

lead_data = generate_fake_leads(5)  # generate 5 leads

print("Step 1 complete: Example lead data generated.")
print("Sample lead record:", lead_data[0])
```

---

## Step 2: Define the Skill for Personalizing Emails

We create and train a skill (using flashlearn, for example), instructing it to generate a personalized email referencing the user’s data and pitching our vertical AI agent for Accounting. The skill will produce a JSON output containing a suggested “subject” and “body” for the email.

### Define an AI Skill for Personalized Emails

We use “LearnSkill” from flashlearn to create a skill that transforms user/lead data into a customized email promoting a vertical AI solution for accounting.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill

def create_email_skill():
    learner = LearnSkill(
        model_name="gpt-4o-mini",  # Example model name
        verbose=True
    )
    
    # Instruction for email generation
    email_instruction = (
        "You are an AI writing outreach emails. The context is a vertical AI agent for Accounting. "
        "For each lead, use the fields (name, company, role, interest_topic, last_contact_date) to create a short, personalized email. "
        "Return JSON with two keys: 'subject' and 'body'. The subject should reference the lead's role/company, "
        "and the body should mention our AI agent for Accounting, referencing any relevant interest_topic. "
        "Keep it friendly, concise, and professional."
    )
    
    # Learn the skill using the lead data and the above instruction
    skill = learner.learn_skill(
        lead_data,
        task=email_instruction,
        model_name="gpt-4o-mini"
    )
    
    return skill

email_skill = create_email_skill()
print("Step 2 complete: Email skill created and learned.")
```

---

## Step 3: Store the Learned Skill as JSON

We serialize (save) the newly created email skill so that we can reload it at any time, avoiding the need to re-learn the instructions and parameters each run.

### Store the Learned Skill in JSON

This ensures we can reuse the same skill definition in the future for consistent email generation.

```python
email_skill_path = os.path.join(json_folder, "accounting_email_skill.json")
email_skill.save(email_skill_path)
print(f"Step 3 complete: Skill saved to {email_skill_path}")
```

---

## Step 4: Load the Saved Skill

When we want to generate emails in a production or separate environment, we simply load the stored skill from JSON, rather than re-learning it.

### Load the Saved Skill

We restore the skill from JSON and ensure it’s ready to generate personalized emails.

```python
email_skill_path = os.path.join(json_folder, "accounting_email_skill.json")
with open(email_skill_path, "r", encoding="utf-8") as file:
    definition = json.load(file)
loaded_email_skill = GeneralSkill.load_skill(definition)
print("Step 4 complete: Skill loaded from JSON:", loaded_email_skill)
```

---

## Step 5: Create Tasks for Email Generation

We transform each lead record into a task that the skill can process. In this example, each field relevant to personalization is simply treated as text or numeric data.

### Create Tasks for Personalized Emails

Each lead is converted into a flashlearn “task.” Label columns if they’re purely textual (e.g., name, company, role).

```python
column_modalities = {
    "name": "text",
    "company": "text",
    "role": "text",
    "interest_topic": "text",
    "last_contact_date": "text"
}

email_tasks = loaded_email_skill.create_tasks(
    lead_data,
    column_modalities=column_modalities
)

print("Step 5 complete: Email tasks created.")
print("Sample email task:", email_tasks[0])
```

---

## Step 6: (Optional) Save Email Tasks to JSONL

We can save the tasks in a JSONL file, which is handy for auditing or offline processing.

### Save Email Tasks to JSONL (Optional)

This preserves the exact tasks so they can be processed later or in another environment.

```python
email_tasks_path = os.path.join(json_folder, "email_tasks.jsonl")
with open(email_tasks_path, 'w') as f:
    for task in email_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Step 6 complete: Email tasks saved to {email_tasks_path}")
```

---

## Step 7: Load Email Tasks from JSONL (Optional)

If we want to separate the task creation from the actual email generation, we can load the tasks from our JSONL file.

### Load Email Tasks from JSONL (Optional)

Demonstrates offline or separate environment usage by reloading tasks.

```python
reloaded_email_tasks = []
with open(email_tasks_path, 'r') as f:
    for line in f:
        reloaded_email_tasks.append(json.loads(line))

print("Step 7 complete: Email tasks reloaded.")
print("Example reloaded task:", reloaded_email_tasks[0])
```

---

## Step 8: Run the Personalized Email Generation

Now we let our skill process all the tasks in parallel (where supported). The AI will create a subject and body for each user, referencing the user’s name, company, last contact, and role.

### Generate Personalized Emails

The skill outputs a JSON object with keys “subject” and “body” for each lead, containing a tailored email.

```python
email_results = loaded_email_skill.run_tasks_in_parallel(reloaded_email_tasks)

print("Step 8 complete: Personalized emails generated.")
print("Sample result (task_id, output):")
for task_id, email_data in list(email_results.items())[:1]:
    print(f"  Task ID {task_id}: {email_data}")
```

---

## Step 9: Map the Generated Emails Back to the Lead Data

We attach the generated email (subject and body) to each original lead record, preserving the context for future steps or direct sending.

### Integrate Email Output with Original Lead Data

We align each AI-generated email with the matching lead, creating a final annotated dataset.

```python
annotated_leads = []
for task_id_str, output_json in email_results.items():
    task_id = int(task_id_str)
    lead_record = lead_data[task_id]
    lead_record["generated_email"] = output_json
    annotated_leads.append(lead_record)

print("Step 9 complete: Email output mapped back to lead data.")
print("Sample annotated lead:", annotated_leads[0])
```

---

## Step 10: Store Final Annotated Results

Finally, we can write these annotated lead records (which now contain both original data and a newly generated email) to a JSONL file for further review or integration into a sending system (like an email marketing tool).

### Store the Final Generated Emails

We save the annotated leads to a JSONL file. Each record now includes the personal email subject and body.

```python
final_emails_path = os.path.join(json_folder, "personalized_emails.jsonl")
with open(final_emails_path, 'w') as f:
    for lead in annotated_leads:
        f.write(json.dumps(lead) + '\n')

print(f"Step 10 complete: Final personalized emails saved to {final_emails_path}")
```

---

## Next Steps
Next steps might involve:  
- Integrating with an actual email marketing service or CRM.  
- Refining prompts or including example-based instruction to improve email quality or style.  
- Segmenting leads by interest or role, then generating different email variations.
