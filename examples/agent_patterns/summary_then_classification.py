import os
import json

from flashlearn.skills import GeneralSkill
from flashlearn.utils import imdb_reviews_50k

def main():
    # 1. Load both “emotional_summary” and “classification” skills
    with open("definitions/emotional_summary.json", "r", encoding="utf-8") as f:
        summary_def = json.load(f)
    summary_skill = GeneralSkill.load_skill(summary_def)

    with open("definitions/classification.json", "r", encoding="utf-8") as f:
        classification_def = json.load(f)
    classification_skill = GeneralSkill.load_skill(classification_def)

    # 2. Load data, remove sentiments
    data = imdb_reviews_50k(full=True)[:1000]
    sentiments = []
    for row in data:
        sentiments.append(row["sentiment"])
        del row["sentiment"]

    # 3. Run "emotional_summary" skill
    tasks_summary = summary_skill.create_tasks(data)
    results_summary = summary_skill.run_tasks_in_parallel(tasks_summary, request_timeout=120)

    # 4. Attach summarized info back into the same data
    for task_id_str, out_sum in results_summary.items():
        tid = int(task_id_str)
        # Our skill should output a key “emotional_summary”
        data[tid]["emotional_summary"] = out_sum.get("emotional_summary", "")

    # 5. Now run classification
    tasks_class = classification_skill.create_tasks(data)
    results_class = classification_skill.run_tasks_in_parallel(tasks_class, request_timeout=120)

    # 6. Compare predictions
    correct = 0
    for task_id_str, out_cls in results_class.items():
        tid = int(task_id_str)
        predicted = out_cls.get("label", "unknown")
        actual = sentiments[tid]
        if predicted == actual:
            correct += 1
        #print(f"Review {tid} => Summary: {data[tid]['emotional_summary']}")
        #print(f"  -> Predicted: {predicted}, Actual: {actual}\n")

    accuracy = correct / len(data) if data else 0
    print(f"[Step 2] Summary → Classification Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()