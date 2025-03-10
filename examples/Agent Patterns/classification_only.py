import os
import json

from flashlearn.skills import GeneralSkill
from flashlearn.utils import imdb_reviews_50k

def main():
    # 1. Load classification skill
    with open("definitions/classification.json", "r", encoding="utf-8") as f:
        classification_def = json.load(f)
    classification_skill = GeneralSkill.load_skill(classification_def)

    # 2. Load IMDB data (remove sentiment for classification)
    data = imdb_reviews_50k(full=True)[:1000]
    sentiments = []
    for row in data:
        sentiments.append(row["sentiment"])
        del row["sentiment"]

    # 3. Run classification
    tasks = classification_skill.create_tasks(data)
    results = classification_skill.run_tasks_in_parallel(tasks, max_requests_per_minute=500,  request_timeout=20)

    # 4. Compare predictions to actual
    correct = 0
    for task_id_str, output in results.items():
        tid = int(task_id_str)
        predicted = output.get("label", "unknown")
        actual = sentiments[tid]
        if predicted == actual:
            correct += 1
        #print(f"Review {tid} => Predicted: {predicted}, Actual: {actual}")

    accuracy = correct / len(data) if data else 0
    print(f"[Step 1] Classification-Only Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()