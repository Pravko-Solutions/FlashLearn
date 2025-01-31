[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
![Pure Python](https://img.shields.io/badge/Python-Pure-blue)  
![Test Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen)  
![Code Size](https://img.shields.io/github/languages/code-size/Pravko-Solutions/FlashLearn)

FlashLearn provides a simple interface and orchestration **(up to 1000 calls/min)** for incorporating **Agent LLMs** into your typical workflows. Conduct data transformations, classifications, summarizations, rewriting, and custom multi-step tasks—just like you’d do with any standard ML library—harnessing the power of LLMs under the hood.

- Usage cookbook [Examples](/examples)  
- Toolkits for advanced, prebuilt transformations: [click](/flashlearn/skills/toolkit)  
- Customization options: [click](/flashlearn/skills/)  

## High-Level Concept Flow

```mermaid
flowchart TB
    H[Data] --> I[Load Skill / Learn Skill]
    I --> J[Create Tasks]
    J --> K[Run Tasks]
    K --> L[Structured Results]
    L --> M[Downstream Steps]
```
---

## Installation

```bash
pip install flashlearn
```

---

## Learning a New “Skill” from Sample Data

Like a fit/predict pattern, you can quickly “learn” a custom skill from minimal (or no!) data. Below, we’ll create a skill that evaluates the likelihood of buying a product from user comments on social media posts, returning a score (1–100) and a short reason. We’ll use a small dataset of comments and instruct the LLM to transform each comment according to our custom specification.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import sample_social_posts
from flashlearn.client import OpenAI

def main():
    # Instantiate your pipeline “estimator” or “transformer”
    learner = LearnSkill(model_name="gpt-4o-mini", client=OpenAI())
    data = sample_social_posts(sample=100)  # Suppose this returns 100 comments

    # Provide instructions and sample data for the new skill
    skill = learner.learn_skill(
        data,
        task=(
            "Evaluate how likely the user is to buy my product based on the sentiment in their comment, "
            "return an integer 1-100 on key 'likely_to_buy', "
            "and a short explanation on key 'reason'."
        ),
    )

    # Construct tasks for parallel execution (akin to batch prediction)
    tasks = skill.create_tasks(data)
    results = skill.run_tasks_in_parallel(tasks)
    print(results)

if __name__ == "__main__":
    main()
```

---

## Input Is a List of Dictionaries

Whether you retrieved data from an API, a spreadsheet, or user-submitted forms, you can simply wrap each record into a dictionary. FlashLearn’s “skills” accept a list of such dictionaries, as shown below:

```python
user_inputs = [
    {"comment_text": "I love this product, it's everything I wanted!"},
    {"comment_text": "Not impressed... wouldn't consider buying this."},
    # ...
]
```

---

## Run in 3 Lines of Code

Once you’ve defined or learned a skill, you can load it as though it were a specialized transformer in a standard ML pipeline. Then apply it to your data in just a few lines:

```python
from flashlearn.skills.general_skill import GeneralSkill

# Suppose we previously saved a learned skill to "evaluate_buy_comments_skill.json".
skill = GeneralSkill.load_skill("evaluate_buy_comments_skill.json")

tasks = skill.create_tasks(user_inputs)
results = skill.run_tasks_in_parallel(tasks)
print(results)
```

---

## Get Structured Results

FlashLearn returns structured outputs for each of your records. The keys in the results dictionary map to the indexes of your original list. For example:

```json
{
  "0": {
    "likely_to_buy": 90,
    "reason": "Comment shows strong enthusiasm and positive sentiment."
  },
  "1": {
    "likely_to_buy": 25,
    "reason": "Expressed disappointment and reluctance to purchase."
  }
}
```

---

## Pass on to Next Steps

Each record’s output can then be used in downstream tasks. For instance, you might:

1. Store the results in a database  
2. Filter for high-likelihood leads  
3. Send them to another tool for further analysis (for example, rewriting the “reason” in a formal tone)

Below is a small example showing how you might parse the dictionary and feed it into a separate function:

```python
# Suppose 'flash_results' is the dictionary with structured LLM outputs
for idx, result in flash_results.items():
    desired_score = result["likely_to_buy"]
    reason_text = result["reason"]
    # Now do something with the score and reason, e.g., store in DB or pass to next step
    print(f"Comment #{idx} => Score: {desired_score}, Reason: {reason_text}")
```

---

## “Skill” Is Just a Simple Dictionary

Internally, a skill is just a compact JSON-like object containing instructions and, optionally, function definitions to strictly validate LLM outputs. You can generate this skill from sample data (as shown above) or create it directly:

```python
EvaluateToBuySkill = {
  "skill_class": "GeneralSkill",
  "system_prompt": "Evaluate how likely the user is to buy our product, returning an integer 1-100 and a short reason.",
  "function_definition": {
    "type": "function",
    "function": {
      "name": "EvaluateToBuySkill",
      "description": "Assess user text with respect to willingness to buy a certain product.",
      "strict": True,
      "parameters": {
        "type": "object",
        "properties": {
          "likely_to_buy": {
            "type": "integer",
            "description": "A number from 1 to 100 indicating how likely the user is to buy."
          },
          "reason": {
            "type": "string",
            "description": "A brief explanation of why this is the likely score."
          }
        },
        "required": ["likely_to_buy", "reason"],
        "additionalProperties": False
      }
    }
  }
}
```

You can load or save this skill to JSON as needed, version it, share it, or plug it into your pipelines. FlashLearn makes the entire process—training, storing, loading, and using such custom LLM transformations—simple and uniform.

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

### Parallel Execution & Cost Estimation
- **Parallel Execution**: `run_tasks_in_parallel` organizes concurrent requests to the LLM.  
- **Cost Estimation**: Quickly preview your token usage:
  ```python
  cost_estimate = skill.estimate_tasks_cost(tasks)
  print("Estimated cost:", cost_estimate)
  ```
---

## Loading a Skill

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
- All code needs at least **95%** test coverage
- Explore the [examples folder](examples/) for more advanced usage patterns.

---

## License

**MIT License**.  
Use it in commercial products, and personal projects.

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

