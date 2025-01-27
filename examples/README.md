# FlashLearn – Examples Directory

This folder contains standalone scripts that demonstrate various features and workflows of the FlashLearn library. Each script is self-contained, showing how to apply skills, discover labels, run batch jobs, classify images, and more—all while maintaining valid JSON responses from Large Language Models (LLMs).

Below you’ll find an overview of each file, what it showcases, and links to the actual code. You can run these examples (assuming you’ve installed FlashLearn and set your “OPENAI_API_KEY”) simply by using:

---

## How to Run

1. Clone or download the FlashLearn repository (or just copy the examples folder).  
2. Install FlashLearn:  
   ```bash
   pip install flashlearn
   ```  
3. Set your “OPENAI_API_KEY” (or other provider keys) in your environment:  
   ```bash
   export OPENAI_API_KEY="YOUR_API_KEY"
   ```
4. Navigate to the “examples” folder and pick any script. Then run, for example:  
   ```bash
   python sentiment_classification.py
   ```
5. Check the console output and JSON results files (e.g., “results.jsonl”).

---

## 1. [batch_api.py](batch_api.py)

Demonstrates how to:
1. Create classification tasks from a JSONL file.  
2. Upload tasks to a Batch API (if supported by your chosen provider).  
3. Retrieve the output once the batch job completes (potentially after hours).

**Key Steps:**
1. Load sample data (IMDB reviews).  
2. Initialize a classification skill.  
3. Create tasks → convert to JSONL → optionally upload for batch processing.  
4. Retrieve results and map them back to the original reviews.  

Use this script if you plan to handle large numbers of tasks asynchronously.

---

## 2. [discover_and_classify_clusters.py](discover_and_classify_clusters.py)

Shows a two-tier approach using:
1. **DiscoverLabelsSkill** – Automatically detect hidden or emergent labels in text data (like IMDB reviews).  
2. **ClassificationSkill** – Utilize previously discovered labels to classify incoming text.

**Core Flow:**
1. Discover unknown categories/clusters (e.g., “funny,” “thrilling,” etc.).  
2. Extract newly found labels.  
3. Initialize a classification skill with those labels.  
4. Apply it to the dataset and see how the discovered categories are assigned.

Ideal if you have unknown or fluid labels that you want the model to uncover before classification.

---

## 3. [image_classification.py](image_classification.py)

Demonstrates image classification with a base64-encoded image column.  
Steps shown in the script:

1. Load a sample dataset of cat and dog images (base64-encoded).  
2. Define a `ClassificationSkill` specifying “cat” and “dog” as categories.  
3. Generate tasks, specifying which columns contain image data.  
4. Run tasks in parallel and analyze the structured JSON results.

You can adapt this approach to any image classification scenario by tweaking the categories and system prompt.

---

## 4. [learn_new_skill.py](learn_new_skill.py)

Showcases how to dynamically “learn” a new classification skill from sample data without fine-tuning the model.  
Uses the `LearnSkill` class, which automates skill generation based on:
1. A set of example data (in this case, IMDB reviews).  
2. A direct prompt describing how to categorize or transform the data.

This is useful when you have a custom theme or specialized categories and want the model to figure out style or category logic from a small sample.

---

## 5. [learn_new_skill_img.py](learn_new_skill_img.py)

Similar to “learn_new_skill.py,” but focused on images.  
Steps:

1. Use `LearnSkill` with image data.  
2. Provide a prompt that instructs the model on how to categorize images (e.g., comedic categories).  
3. Generate tasks specifying the “image_base64” data.  
4. Apply the newly learned skill to unseen images.

Useful if your project needs dynamic or custom labeling for images—beyond standard “cat vs. dog.”

---

## 6. [load_skill.py](load_skill.py)

Highlights loading a “predefined skill” from the FlashLearn library or a JSON file.  
Key points:

1. Demonstrates how to use `GeneralSkill.load_skill(...)` to quickly instantiate a skill from a built-in or previously saved definition.  
2. Creates tasks from sample data and runs them in parallel.  
3. Perfect for reusing skill definitions across multiple scripts or microservices without rewriting prompts.

---

## 7. [load_skill_img.py](load_skill_img.py)

A variant of “load_skill.py” for image tasks.  
Steps:

1. Loads a JSON skill definition that handles images.  
2. Uses `GeneralSkill.load_skill(...)` to deserialize the skill definition.  
3. Classifies or processes base64-encoded images in real time.  

Great if you have a saved skill configuration (e.g., “MyCustomSkillIMG.json”) and want to apply it to new images on the fly.

---

## 8. [sentiment_classification.py](sentiment_classification.py)

A complete walk-through on performing sentiment classification (e.g., “positive” or “negative”) on IMDB reviews in real time (not batch).  
Showcases:

1. Initializing a `ClassificationSkill` with an LLM client.  
2. Generating tasks from raw data.  
3. Executing tasks in parallel.  
4. Mapping results back and calculating accuracy vs. ground truth.  
5. Saving results and the skill definition to JSON/JSONL for future reference.

This is a great starting point for anyone wanting an end-to-end text classification pipeline that yields JSON outputs.

---

## 9. [tests/integration_test.py](tests/integration_test.py)

Not a standard example script, but rather a simple integration test that:
1. Iterates through all Python files in this examples folder.  
2. Attempts to run each script.  
3. Prints the output or errors.

Use this if you want to quickly ensure all examples run in your environment without manually invoking each one.

---

## Next Steps

• Modify any example to fit your own data or tasks.  
• Explore the [FlashLearn GitHub repository](https://github.com/Pravko-Solutions/FlashLearn) for advanced usage and debugging tips.  
• Consult the top-level documentation for details on concurrency, cost estimation, and building custom or advanced Skills.

Happy experimenting with FlashLearn examples! If you need further support or consulting, check the links in the main documentation.