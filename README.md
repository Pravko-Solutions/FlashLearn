# FlashLearn - Agents made simple

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Pure Python](https://img.shields.io/badge/Python-Pure-blue)
![Test Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen)
![Code Size](https://img.shields.io/github/languages/code-size/Pravko-Solutions/FlashLearn)

FlashLearn provides a simple interface and orchestration **(up to 1000 calls/min)** for incorporating **Agent LLMs** into your typical workflows. Conduct data transformations, classifications, summarizations, rewriting, and custom multi-step tasks—**just like you’d do with any standard ML library**, but harnessing the power of LLMs under the hood.

- Examples: [click](/examples)
- Toolkits for advanced, prebuilt transformations: [click](/flashlearn/skills/toolkit)  
- Customization options: [click](/flashlearn/skills/)  

Install:
--------------------------------------------------------------------------------
```bash
pip install flashlearn
```
## Perplexity clone in 10 lines of code
```python
question = 'When was python launched?'
skill = GeneralSkill.load_skill(ConvertToGoogleQueries, client=OpenAI())
queries = skill.run_tasks_in_parallel(skill.create_tasks([{"query": question}]))["0"]
results = SimpleGoogleSearch(GOOGLE_API_KEY, GOOGLE_CSE_ID).search(queries['google_queries'])
msgs = [
    {"role": "system", "content": "insert links from search results in response to quote it"},
    {"role": "user", "content": str(results)},
    {"role": "user", "content": question},
]
print(client.chat.completions.create(model=MODEL_NAME, messages=msgs).choices[0].message.content)
```
## "Skill" is just a simple dictionary
A skill is an LLM's ability to perform a task, containing all necessary information. You can create, use predefined, or generate skills from sample data.

```python
ConvertToGoogleQueries = {
  "skill_class": "GeneralSkill",
  "system_prompt": "Exactly populate the provided function definition",
  "function_definition": {
    "type": "function",
    "function": {
      "name": "ConvertToGoogleQueries",
      "description": "Convert the given question into between 1 and n google queries to answer the given question.",
      "strict": True,
      "parameters": {
        "type": "object",
        "properties": {
          "google_queries": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "google_queries"
        ],
        "additionalProperties": False
      }
    }
  }
}
```
## Run in 3 lines of code
Load “skills” as if they were specialized transformers in a ML pipeline. Instantly apply them to your data:

```python
# You can pass client to load your pipeline component
skill = GeneralSkill.load_skill(ConvertToGoogleQueries)
tasks = skill.create_tasks([{"query": "Users query"}])
results = skill.run_tasks_in_parallel(tasks)

print(results)
```

## Get structured results
Get structured results to be used in downstream tasks.
```python
results = {'0':{'google_queries': [QUERY_1, QUERY_2, ...]}}

```
## Learning a New “Skill” from Sample Data
Like fit/predict pattern, you can quickly “learn” a custom skill from minimal (or no!) data. Provide sample data and instructions, then immediately apply to new inputs.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import imdb_reviews_50k

def main():
    # Instantiate your pipeline “estimator” or “transformer”
    learner = LearnSkill(model_name="gpt-4o-mini", clinet=OpenAI())
    data = imdb_reviews_50k(sample=100)

    # Provide instructions and sample data for the new skill
    skill = learner.learn_skill(
        data,
        task=(
            'Evaluate likelihood to buy my product and write the reason why (on key "reason")'
            'return int 1-100 on key "likely_to_Buy".'
        ),
    )

    # Construct tasks for parallel execution (akin to batch prediction)
    tasks = skill.create_tasks(data)
    results = skill.run_tasks_in_parallel(tasks)
    print(results)
```
--------------------------------------------------------------------------------
## Single-Step Classification Using Prebuilt Skills
Classic classification tasks are as straightforward as calling “fit_predict” on a ML estimator:
• Toolkits for advanced, prebuilt transformations: [click](/flashlearn/skills/toolkit)  

```python
import os
from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
data = [{"message": "Where is my refund?"}, {"message": "My product was damaged!"}]

skill = ClassificationSkill(
    model_name="gpt-4o-mini",
    client=OpenAI(),
    categories=["billing","product issue"],
    system_prompt="Classify the request."
)

tasks = skill.create_tasks(data)
print(skill.run_tasks_in_parallel(tasks))
```

## Supported LLM Providers
Anywhere you might rely on an ML pipeline component, you can swap in an LLM:
```python
client = OpenAI()  # This is equivalent to instantiating a pipeline component 
deep_seek = OpenAI(api_key='YOUR DEEPSEEK API KEY', base_url="https://api.deepseek.com")
lite_llm = FlashLiteLLMClient()  # LiteLLM integration Manages keys as environment variables, akin to a top-level pipeline manager
```

## Target audience
- Anyone needing LLM-based data transformations at scale
- Data scientists tired of building specialized models with insufficient data

[![Support & Consulting](https://img.shields.io/badge/Support%20%26%20Consulting-Click%20Here-brightgreen)](https://calendly.com/flashlearn)

---

## Key Features 

- **100% JSON Workflows**: Every response is valid JSON—machine-friendly from the start.  
- **Scales Easily**: Concurrency and rate limiting for large-scale projects.  
- **Zero Model Training**: Leverage your LLM directly; define or reuse “skills.”  
- **LearnSkill**: Instant creation of classification/rewriting “skills” from sample data.  
- **Batch or Real-Time**: Process live data, or batch thousands of tasks.  
- **Cost Estimation**: Predict token expenditures before running large jobs.  
- **Skill Library**: 200+ built-in skill definitions ([docs](flashlearn/skills/toolkit)).  
- **Multi-Modal**: Handle text, images, and more in consistent JSON pipelines.

## High-throughput
Process up to 999 tasks in 60 seconds on your local machine. For higher loads and enterprise needs contact us for enterprise solution.
[![Enterprise Edition Demo](https://img.shields.io/badge/Enterprise%20Edition%20Demo-Click%20Here-blue)](https://calendly.com/flashlearn/enterprise-demo)

```text
Processing tasks in parallel: 100%|██████████| 999/999 [01:00<00:00, 16.38 it/s, In total: 368969, Out total: 17288]
INFO:ParallelProcessor:All tasks complete. 999 succeeded, 0 failed.
```
## High-Level Concept Flow

1. Convert data rows into JSON tasks.  
2. Apply a Skill (classification, rewriting, etc.).  
3. LLM outputs guaranteed JSON.  
4. (Optional) Store or chain the JSON results into your next step.

```
Dataset Rows → JSON Tasks → FlashLearn Skills + LLM → Guaranteed JSON → DB/Next Steps
```

With guaranteed JSON, there’s no need to parse unstructured text. You can immediately save each result to your database or pass it to another pipeline stage.

---

## Installation

1. Install via PyPI:  
   ```bash
   pip install flashlearn
   ```

2. Set up your LLM provider (OpenAI, DeepSeek, etc.):  
   ```bash
   export OPENAI_API_KEY="YOUR_API_KEY"
   ```
   Or define a `base_url` for an open-source endpoint.

---

## “All JSON, All the Time”: Example Classification Workflow

The following example classifies IMDB movie reviews into “positive” or “negative” sentiment. Notice how at each step you can view, store, or chain the partial results—always in JSON format.

```python
from flashlearn.utils import imdb_reviews_50k
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import ClassifyReviewSentiment
import json
import os

def main():
    os.environ["OPENAI_API_KEY"] = "API-KEY"

    # Step 1: Load or generate your data
    data = imdb_reviews_50k(sample=100)  # 100 sample reviews

    # Step 2: Load JSON definition of skill in dict format
    skill = GeneralSkill.load_skill(ClassifyReviewSentiment)
        
    # Step 3: Save skill definition in JSON for later loading
    #skill.save("BinaryClassificationSkill.json")
    
    # Step 5: Convert data rows into JSON tasks
    tasks = skill.create_tasks(data)
    
    # Step 6: Save results to a JSONL file and run now or later
    with open('tasks.jsonl', 'w') as jsonl_file:
        for entry in tasks:
            jsonl_file.write(json.dumps(entry) + '\n')
            
    # Step 7: Run tasks (in parallel by default)
    results = skill.run_tasks_in_parallel(tasks)

    # Step 8: Every output is strict JSON
    # You can easily map results back to inputs
    # e.g., store results as JSON Lines
    with open('sentiment_results.jsonl', 'w') as f:
        for task_id, output in results.items():
            input_json = data[int(task_id)]
            input_json['result'] = output
            f.write(json.dumps(input_json) + '\n')

    # Step 9: Inspect or chain the JSON results
    print("Sample result:", results.get("0"))

if __name__ == "__main__":
    main()
```

The output is consistently keyed by task ID (`"0"`, `"1"`, etc.), with the JSON content that your pipeline can parse or store with no guesswork.

---

## Use Cases & Real Examples

### Discover & Classify Clusters
1. **DiscoverLabelsSkill** automatically identifies emerging labels in text.  
2. Feed the discovered labels into a standard classification skill.  
3. Scale your labeling process quickly, with minimal human effort.

### JSON Function Calls (GeneralSkill)
Skills define JSON schemas so the LLM must respond in valid JSON. Examples include rewriting text in comedic form, extracting docstrings, or providing bullet-point lists.

```python
import json
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import ClassifyDifficultyOfQuestion

def main():
    # Load a pre-defined skill from the toolkit
    skill = GeneralSkill.load_skill(ClassifyDifficultyOfQuestion)
    tasks = skill.create_tasks([{"text": "What is 12 squared?"}])
    results = skill.run_tasks_in_parallel(tasks)
    print(results)
```

Result is valid JSON like:
```json
{"difficulty": "easy"}
```
No disclaimers or random text—just structured data.
[![Support & Consulting](https://img.shields.io/badge/Support%20%26%20Consulting-Click%20Here-brightgreen)](https://calendly.com/flashlearn)

---

## Image Classification Example

```python
from flashlearn.skills.classification import ClassificationSkill

def main():
    images = [...]  # base64-encoded images
    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        categories=["cat", "dog"],
        system_prompt="Classify images as 'cat' or 'dog'."
    )
    column_modalities = {"image_base64": "image_base64"}
    tasks = skill.create_tasks(images, column_modalities=column_modalities)
    results = skill.run_tasks_in_parallel(tasks)
    print(results)
```

You’ll have JSON results, e.g. `{"category": "cat"}` for each image, which you can export as `.jsonl` or pass to another system.
[![Support & Consulting](https://img.shields.io/badge/Support%20%26%20Consulting-Click%20Here-brightgreen)](https://calendly.com/flashlearn)

---

## How It Works

### Skills
A “Skill” encapsulates:  
- Which LLM to call (OpenAI, local, or custom).  
- System prompt or instructions.  
- JSON schema or format constraints.  
- Methods to parse the LLM response safely into JSON.

### Tasks
Each piece of data is a “Task,” which is turned into a JSON prompt for the LLM. When run in parallel, tasks are grouped into requests respecting concurrency limits.

### All JSON, All the Time
With FlashLearn, the LLM must output JSON. You’re never stuck parsing disclaimers, messy text, or swirling disclaimers. You can intercept and store partial or final results in JSON. This is critical for robust pipelines, especially when chaining multiple steps.

### Parallel Execution & Cost Estimation
- **Parallel Execution**: `run_tasks_in_parallel` organizes concurrent requests to the LLM.  
- **Cost Estimation**: Quickly preview your token usage:
  ```python
  cost_estimate = skill.estimate_tasks_cost(tasks)
  print("Estimated cost:", cost_estimate)
  ```

---

## Loading & Customizing a Skill

Here’s how the library handles comedic rewrites:

```python
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import HumorizeText

def main():
    data = [{"original_text": "We are behind schedule."}]
    skill = GeneralSkill.load_skill(HumorizeText)
    tasks = skill.create_tasks(data)
    results = skill.run_tasks_in_parallel(tasks)
    print(results)
```

You’ll see output like:
```json
{
  "0": {
    "comedic_version": "Hilarious take on your sentence..."
  }
}
```
Everything is well-structured JSON, suitable for further analysis.

---

##  Contributing & Community

- Licensed under MIT.  
- [Fork us](flashlearn/) to add new skills, fix bugs, or create new examples.  
- We aim to make robust LLM workflows accessible to all startups.  
- All code needs at least **95%** tests coverage
- Explore the [examples folder](examples/) for more advanced usage patterns.

---

## License

**MIT License**.  
Use it in commercial products, personal projects.

---

## “Hello World” Demos

### Image Classification

```python
import os
from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import cats_and_dogs

def main():
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'
    data = cats_and_dogs(sample=6)

    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        client=OpenAI(),
        categories=["cat", "dog"],
        max_categories=1,
        system_prompt="Classify what's in the picture."
    )

    column_modalities = {"image_base64": "image_base64"}
    tasks = skill.create_tasks(data, column_modalities=column_modalities)
    results = skill.run_tasks_in_parallel(tasks)
    print(results)

    # Save skill definition for reuse
    skill.save("MyCustomSkillIMG.json")

if __name__ == "__main__":
    main()
```

### Text Classification

```python
import json
import os
from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import imdb_reviews_50k

def main():
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'
    reviews = imdb_reviews_50k(sample=100)

    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        client=OpenAI(),
        categories=["positive", "negative"],
        max_categories=1,
        system_prompt="Classify short movie reviews by sentiment."
    )

    # Convert each row into a JSON-based task
    tasks = skill.create_tasks([{'review': x['review']} for x in reviews])
    results = skill.run_tasks_in_parallel(tasks)

    # Compare predicted sentiment with ground truth for accuracy
    correct = 0
    for i, review in enumerate(reviews):
        predicted = results[str(i)]['categories']
        reviews[i]['predicted_sentiment'] = predicted
        if review['sentiment'] == predicted:
            correct += 1

    print(f'Accuracy: {round(correct / len(reviews), 2)}')

    # Store final results as JSON Lines
    with open('results.jsonl', 'w') as jsonl_file:
        for entry in reviews:
            jsonl_file.write(json.dumps(entry) + '\n')

    # Save the skill definition
    skill.save("BinaryClassificationSkill.json")

if __name__ == "__main__":
    main()
```

---

## Final Words

FlashLearn brings clarity to LLM workflows by enforcing consistent JSON output at every step. Whether you run a single classification or a multi-step pipeline, you can store partial results, debug easily, and maintain confidence in your data.  
[![Support & Consulting](https://img.shields.io/badge/Support%20%26%20Consulting-Click%20Here-brightgreen)](https://calendly.com/flashlearn)

