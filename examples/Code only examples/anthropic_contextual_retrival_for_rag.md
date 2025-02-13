RAG quality is pain and a while ago Antropic proposed contextual retrival implementation. In a nutshell, this means that you take your chunk and full document and generate extra context for the chunk and how it's situated in the full document, and then you embed this text to embed as much meaning as possible.

**Key idea: Instead of embedding just a chunk, you generate a context of how the chunk fits in the document and then embed it together.**

Below is a full implementation of generating such context that you can later use in your RAG pipelines to improve retrieval quality.  

The process captures contextual information from document chunks using an AI skill, enhancing retrieval accuracy for document content stored in Knowledge Bases.

## Step 0: Environment Setup

First, set up your environment by installing necessary libraries and organizing storage for JSON artifacts.

```python
import os
import json

# (Optional) Set your API key if your provider requires one.
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Create a folder for JSON artifacts
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Environment setup.")
```

---

## Step 1: Prepare Input Data

Create synthetic or real data mimicking sections of a document and its chunk.

```python
contextual_data = [
    {
        "full_document": (
            "In this SEC filing, ACME Corp reported strong growth in Q2 2023. "
            "The document detailed revenue improvements, cost reduction initiatives, "
            "and strategic investments across several business units. Further details "
            "illustrate market trends and competitive benchmarks."
        ),
        "chunk_text": (
            "Revenue increased by 5% compared to the previous quarter, driven by new product launches."
        )
    },
    # Add more data as needed
]

print("Step 1 complete: Contextual retrieval data prepared.")
```

---

## Step 2: Define AI Skill

Utilize a library such as flashlearn to define and learn an AI skill for generating context.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill

def create_contextual_retrieval_skill():
    learner = LearnSkill(
        model_name="gpt-4o-mini",  # Replace with your preferred model
        verbose=True
    )
    
    contextual_instruction = (
        "You are an AI system tasked with generating succinct context for document chunks. "
        "Each input provides a full document and one of its chunks. Your job is to output a short, clear context "
        "(50–100 tokens) that situates the chunk within the full document for improved retrieval. "
        "Do not include any extra commentary—only output the succinct context."
    )
    
    skill = learner.learn_skill(
        df=[],  # Optionally pass example inputs/outputs here
        task=contextual_instruction,
        model_name="gpt-4o-mini"
    )
    
    return skill

contextual_skill = create_contextual_retrieval_skill()
print("Step 2 complete: Contextual retrieval skill defined and created.")
```

---

## Step 3: Store AI Skill

Save the learned AI skill to JSON for reproducibility.

```python
skill_path = os.path.join(json_folder, "contextual_retrieval_skill.json")
contextual_skill.save(skill_path)
print(f"Step 3 complete: Skill saved to {skill_path}")
```

---

## Step 4: Load AI Skill

Load the stored AI skill from JSON to make it ready for use.

```python
with open(skill_path, "r", encoding="utf-8") as file:
    definition = json.load(file)
loaded_contextual_skill = GeneralSkill.load_skill(definition)
print("Step 4 complete: Skill loaded from JSON:", loaded_contextual_skill)
```

---

## Step 5: Create Retrieval Tasks

Create tasks using the loaded AI skill for contextual retrieval.

```python
column_modalities = {
    "full_document": "text",
    "chunk_text": "text"
}

contextual_tasks = loaded_contextual_skill.create_tasks(
    contextual_data,
    column_modalities=column_modalities
)

print("Step 5 complete: Contextual retrieval tasks created.")
```

---

## Step 6: Save Tasks

Optionally, save the retrieval tasks to a JSON Lines (JSONL) file.

```python
tasks_path = os.path.join(json_folder, "contextual_retrieval_tasks.jsonl")
with open(tasks_path, 'w') as f:
    for task in contextual_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Step 6 complete: Contextual retrieval tasks saved to {tasks_path}")
```

---

## Step 7: Load Tasks

Reload the retrieval tasks from the JSONL file, if necessary.

```python
loaded_contextual_tasks = []
with open(tasks_path, 'r') as f:
    for line in f:
        loaded_contextual_tasks.append(json.loads(line))

print("Step 7 complete: Contextual retrieval tasks reloaded.")
```

---

## Step 8: Run Retrieval Tasks

Execute the retrieval tasks and generate contexts for each document chunk.

```python
contextual_results = loaded_contextual_skill.run_tasks_in_parallel(loaded_contextual_tasks)
print("Step 8 complete: Contextual retrieval finished.")
```

---

## Step 9: Map Retrieval Output

Map generated context back to the original input data.

```python
annotated_contextuals = []
for task_id_str, output_json in contextual_results.items():
    task_id = int(task_id_str)
    record = contextual_data[task_id]
    record["contextual_info"] = output_json  # Attach the generated context
    annotated_contextuals.append(record)

print("Step 9 complete: Mapped contextual retrieval output to original data.")
```

---

## Step 10: Save Final Results

Save the final annotated results, with contextual info, to a JSONL file for further use.

```python
final_results_path = os.path.join(json_folder, "contextual_retrieval_results.jsonl")
with open(final_results_path, 'w') as f:
    for entry in annotated_contextuals:
        f.write(json.dumps(entry) + '\n')

print(f"Step 10 complete: Final contextual retrieval results saved to {final_results_path}")
```

# Full Code
```python
import os
import json

# (Optional) Set your API key if your provider requires one.
os.environ["OPENAI_API_KEY"] = "sk-proj-...."  # Replace with your actual API key

# Create a folder for JSON artifacts (skill definitions, tasks, and final results)
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

# --- Step 2 Below: Import flashlearn components ---
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill


def create_contextual_retrieval_skill():
    """
    Create an AI skill that generates succinct context for a document chunk.
    The skill takes two keys (full_document and chunk_text) as input and returns a short
    context (50–100 tokens) that situates the chunk in the full document.
    """
    learner = LearnSkill(
        model_name="gpt-4o-mini",  # Replace with your preferred model
        verbose=True
    )

    contextual_instruction = (
        "You are an AI system tasked with generating succinct context for document chunks. "
        "Each input provides a full document and one of its chunks. Your job is to output a short, clear context "
        "(50–100 tokens) that situates the chunk within the full document for improved retrieval. "
        "Do not include any extra commentary—only output the succinct context. On key full context"
    )

    skill = learner.learn_skill(
        df=[],  # You can optionally pass example inputs/outputs here
        task=contextual_instruction,
        model_name="gpt-4o-mini"
    )

    return skill


def main():
    # --- Step 0: Environment Setup ---
    print("Step 0 complete: Environment setup.")

    # --- Step 1: Prepare Contextual Retrieval Data ---
    # Each dictionary contains a 'full_document' and a 'chunk_text'.
    contextual_data = [
        {
            "full_document": (
                "In this SEC filing, ACME Corp reported strong growth in Q2 2023. "
                "The document detailed revenue improvements, cost reduction initiatives, "
                "and strategic investments across several business units. Further details "
                "illustrate market trends and competitive benchmarks."
            ),
            "chunk_text": (
                "Revenue increased by 5% compared to the previous quarter, driven by new product launches."
            )
        },
        {
            "full_document": (
                "The annual report of BetaTech Inc. summarizes the company’s performance and strategic shifts. "
                "Key highlights include diversification of its portfolio, a shift in resource allocation, "
                "and a gradual improvement in profit margins. Financial figures are elaborated in subsequent sections."
            ),
            "chunk_text": (
                "Profit margins improved subtly following reallocation of resources in the second half of the year."
            )
        }
    ]

    print("Step 1 complete: Contextual retrieval data prepared.")
    print("Sample data entry:", contextual_data[0])

    # --- Step 2: Define an AI Skill for Contextual Retrieval ---
    contextual_skill = create_contextual_retrieval_skill()
    print("Step 2 complete: Contextual retrieval skill defined and created.")

    # --- Step 3: Save the Learned Skill as JSON ---
    skill_path = os.path.join(json_folder, "contextual_retrieval_skill.json")
    contextual_skill.save(skill_path)
    print(f"Step 3 complete: Skill saved to {skill_path}")

    # --- Step 4: Load the Saved Skill ---
    with open(skill_path, "r", encoding="utf-8") as file:
        definition = json.load(file)
    loaded_contextual_skill = GeneralSkill.load_skill(definition)
    print("Step 4 complete: Skill loaded from JSON:", loaded_contextual_skill)

    # --- Step 5: Create Contextual Retrieval Tasks ---
    # Define the column modalities for the fields in our data.
    column_modalities = {
        "full_document": "text",
        "chunk_text": "text"
    }

    contextual_tasks = loaded_contextual_skill.create_tasks(
        contextual_data,
        column_modalities=column_modalities
    )

    print("Step 5 complete: Contextual retrieval tasks created.")
    print("Sample retrieval task:", contextual_tasks[0])

    # --- Step 6: (Optional) Save Tasks to JSONL ---
    tasks_path = os.path.join(json_folder, "contextual_retrieval_tasks.jsonl")
    with open(tasks_path, 'w') as f:
        for task in contextual_tasks:
            f.write(json.dumps(task) + '\n')

    print(f"Step 6 complete: Contextual retrieval tasks saved to {tasks_path}")

    # --- Step 7: Load Tasks from JSONL (Optional) ---
    loaded_contextual_tasks = []
    with open(tasks_path, 'r') as f:
        for line in f:
            loaded_contextual_tasks.append(json.loads(line))

    print("Step 7 complete: Contextual retrieval tasks reloaded.")
    print("Sample reloaded task:", loaded_contextual_tasks[0])

    # --- Step 8: Run the Contextual Retrieval Tasks ---
    contextual_results = loaded_contextual_skill.run_tasks_in_parallel(loaded_contextual_tasks)
    print("Step 8 complete: Contextual retrieval finished.")
    print("Sample result (task_id, output):")
    for task_id, context_output in list(contextual_results.items())[:1]:
        print(f"  Task ID {task_id}: {context_output}")

    # --- Step 9: Map the Retrieval Output Back to the Original Data ---
    annotated_contextuals = []
    for task_id_str, output_json in contextual_results.items():
        task_id = int(task_id_str)
        record = contextual_data[task_id]
        record["contextual_info"] = output_json  # Attach the generated context
        annotated_contextuals.append(record)

    print("Step 9 complete: Mapped contextual retrieval output to original data.")
    print("Annotated record example:", annotated_contextuals[0])

    # --- Step 10: Save the Final Annotated Results ---
    final_results_path = os.path.join(json_folder, "contextual_retrieval_results.jsonl")
    with open(final_results_path, 'w') as f:
        for entry in annotated_contextuals:
            f.write(json.dumps(entry) + '\n')

    print(f"Step 10 complete: Final contextual retrieval results saved to {final_results_path}")


if __name__ == "__main__":
    main()

```

Now you can embed this extra context next to chunk data to improve retrieval quality.
