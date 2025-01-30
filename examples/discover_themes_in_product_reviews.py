import os
from openai import OpenAI
from flashlearn.skills.discover_labels import DiscoverLabelsSkill
from flashlearn.skills.classification import ClassificationSkill

def main():

    os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

    # Example data (text reviews)

    text_reviews = [

        {"comment": "Battery life exceeded expectations, though camera was mediocre."},

        {"comment": "Arrived late and cracked screen, but customer support was helpful."}

    ]

    # Example data (images + brief text)

    # Here, the "image_base64" field simulates an encoded image

    image_reviews = [

        {"image": "ENCODED_ISSUE_IMAGE", "comment": "WHZ BOTHER WITH IT?"},

        {"image": "ENCODED_ISSUE_IMAGE", "comment": "This feature is amazing!! You should charge more!"}

    ]

    # 1) Label Discovery (Aggregates the entire dataset at once)

    discover_skill = DiscoverLabelsSkill(model_name="gpt-4o-mini", client=OpenAI())

    column_modalities={"image_base64":"image_base64", "comment": "text"}

    tasks_discover = discover_skill.create_tasks(text_reviews + image_reviews)

    discovered_labels = discover_skill.run_tasks_in_parallel(tasks_discover)['0']['labels']

    print("Discovered labels:", discovered_labels)

    # 2) Classification using discovered labels

    classify_skill = ClassificationSkill(model_name="gpt-4o-mini", client=OpenAI(), categories=discovered_labels)

    tasks_classify = classify_skill.create_tasks(text_reviews + image_reviews)

    final_results = classify_skill.run_tasks_in_parallel(tasks_classify)

    print("Classification results:", final_results)

if __name__ == "__main__":

    main()
