# Sentiment Classification
## Pro tip: Ctrl + C -> ChatGPT -> Ctrl + V -> Describe your problem-> Get your code
---

## Step 0: Imports and Environment Setup

We begin by importing the necessary libraries, setting environment variables (if needed), and preparing any directories for storing JSON artifacts (e.g., skill files, tasks, and final results).

### Environment Setup

Import libraries, set API keys if necessary, and optionally create folders for storing JSON artifacts.

```python
import json
import os

from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import imdb_reviews_50k

# (Optional) Ensure your API key is set if you're using OpenAI as a provider
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Create a folder for JSON artifacts if desired
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Environment setup.")
```

---

## Step 1: Setup Your Provider

We configure our client, which in this case is openai.OpenAI. You can replace the keys or base URL if you’re using a different deployment or custom endpoint.

### Setup Your Provider

Here, we prepare the AI provider (e.g., OpenAI) for classification tasks.

```python
def get_provider():
    # If you have a custom base_url or API key, set it here
    # deep_seek = OpenAI(
    #     api_key='YOUR DEEPSEEK API KEY',
    #     base_url="https://api.deepseek.com",
    # )
    client = OpenAI()
    return client

print("Step 1 complete: Provider ready.")
```

---

## Step 2: Load Sample Data

We use `flashlearn.utils.imdb_reviews_50k` to load a sample of IMDB movie reviews. Each item in the returned list is a dictionary containing, typically, "review" (the text) and "sentiment" (the true label).

### Load Sample Data

We pull 100 IMDB reviews for demonstration. Each record has a "review" string and "sentiment" label.

```python
client = get_provider()

# Load 100 reviews from IMDB
reviews = imdb_reviews_50k(sample=100)
print(f"Step 2 complete: Loaded {len(reviews)} sample reviews.")
print("Sample review:", reviews[0])
```

---

## Step 3: Initialize the Classification Skill

We create a `ClassificationSkill`, specifying model parameters, the fixed categories (“positive” and “negative”), and a system prompt clarifying the classification instructions.

### Initialize the Classification Skill

We configure the target categories, maximum number of categories (1 in this case), and supply a prompt describing the desired sentiment classification.

```python
skill = ClassificationSkill(
    model_name="gpt-4o-mini",   # or "deepseek-chat", etc.
    client=client,
    categories=["positive", "negative"],
    max_categories=1,
    system_prompt="We want to classify short movie reviews by sentiment."
)

print("Step 3 complete: Classification skill initialized.")
```

---

## Step 4: Prepare Classification Tasks

We remove the “sentiment” label for classification to replicate a real inference scenario. We then transform this data into tasks recognized by the skill. Finally, we store the tasks in a JSONL file for auditing or offline processing.

### Prepare Classification Tasks

In this step, we remove the ground truth sentiment from each review, generate tasks, and save them in a JSONL file.

```python
# Remove the sentiment to simulate unlabeled data
removed_sentiment = [{"review": x["review"]} for x in reviews]

# Create tasks
tasks = skill.create_tasks(removed_sentiment)

# Save tasks to JSONL for reproducibility
tasks_jsonl_path = os.path.join(json_folder, "tasks.jsonl")
with open(tasks_jsonl_path, 'w') as jsonl_file:
    for entry in tasks:
        jsonl_file.write(json.dumps(entry) + '\n')

print(f"Step 4 complete: Classification tasks created and saved to {tasks_jsonl_path}")
```

---

## Step 5: Execute Classification Tasks

We pass the tasks to the skill, which infers the sentiment for each review. The function `run_tasks_in_parallel` processes them either concurrently or sequentially behind the scenes.

### Execute Classification Tasks

We run our tasks to produce sentiment predictions for each review.

```python
results = skill.run_tasks_in_parallel(tasks)
print("Step 5 complete: Classification tasks executed.")
print("Sample classification result:", list(results.items())[0])
```

---

## Step 6: Map Results and Check Accuracy

We attach each predicted category to the original dataset and compare it against the known “sentiment” label to compute accuracy.

### Map Results and Check Accuracy

We add the model’s predicted category to each review record, then compute the fraction of correct classifications.

```python
correct = 0
for i, review in enumerate(reviews):
    predicted_category = results[str(i)]["categories"]
    reviews[i]["category"] = predicted_category
    if review["sentiment"] == predicted_category:
        correct += 1

accuracy = round(correct / len(reviews), 2)
print(f"Step 6 complete: Accuracy = {accuracy * 100}%")
```

---

## Step 7: Save Final Results to a JSONL File

Finally, we store the updated reviews (including predicted labels) to a JSONL file, preserving both the original data and our classification outputs.

### Save Final Results

We write the annotated (predicted) reviews to another JSONL, making it easy to review or feed into subsequent processes.

```python
results_jsonl_path = os.path.join(json_folder, "results.jsonl")
with open(results_jsonl_path, 'w') as jsonl_file:
    for entry in reviews:
        jsonl_file.write(json.dumps(entry) + '\n')

print(f"Step 7 complete: Final results saved to {results_jsonl_path}")
```

---

## Step 8: Save the Skill Configuration

We serialize the `ClassificationSkill` definition for future re-use. This allows you to load and re-run the exact same classification logic without re-initializing or re-configuring.

### Save the Skill Configuration

We store the skill as a JSON file to ensure reproducibility and allow offline usage or sharing.

```python
skill.save("BinaryClassificationSkill.json")
print("Step 8 complete: Skill configuration saved to BinaryClassificationSkill.json")
```

---

## Full Code

Below is the full, consolidated Python script for reference:

```python
import json
import os

from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import imdb_reviews_50k

def main():
    # Step 1: Setup your provider
    # os.environ["OPENAI_API_KEY"] = 'YOUR_API_KEY'
    client = OpenAI()

    # Step 2: Load sample data
    reviews = imdb_reviews_50k(sample=100)

    # Step 3: Initialize the Classification Skill
    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        client=client,
        categories=["positive", "negative"],
        max_categories=1,
        system_prompt="We want to classify short movie reviews by sentiment."
    )

    # Step 4: Prepare classification tasks
    removed_sentiment = [{'review': x['review']} for x in reviews]
    tasks = skill.create_tasks(removed_sentiment)
    with open('tasks.jsonl', 'w') as jsonl_file:
        for entry in tasks:
            jsonl_file.write(json.dumps(entry) + '\n')

    # Step 5: Execute classification tasks
    results = skill.run_tasks_in_parallel(tasks)

    # Step 6: Map results and check accuracy
    correct = 0
    for i, review in enumerate(reviews):
        predicted_category = results[str(i)]['categories']
        reviews[i]['category'] = predicted_category
        if reviews[i]['sentiment'] == predicted_category:
            correct += 1
    print(f'Accuracy: {round(correct / len(reviews), 2) * 100}%')

    # Step 7: Save results to a JSONL file
    with open('results.jsonl', 'w') as jsonl_file:
        for entry in reviews:
            jsonl_file.write(json.dumps(entry) + '\n')

    # Step 8: Save the Skill configuration
    skill.save("BinaryClassificationSkill.json")

if __name__ == "__main__":
    main()
```

---

## Summary and Next Steps

By following this tutorial, you have:  
1. Configured an OpenAI-like client.  
2. Loaded IMDb movie reviews.  
3. Created a sentiment classification skill.  
4. Generated classification tasks and stored them as JSONL.  
5. Executed classification, checked accuracy, and stored final results.  
6. Saved the skill configuration for future re-use.

You can adapt or extend this approach by:  
- Incorporating additional sentiment categories (like “neutral”).  
- Creating downstream tasks based on the predicted sentiment (e.g., filtering content, triggering alerts).

This completes our step-by-step guide for classifying IMDb reviews using Flashlearn’s ClassificationSkill!
