import os
from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import cats_and_dogs

def main():
    # Step 1: Provide your OpenAI
    #os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    # Step 2: Load sample image data in base64 format
    data = cats_and_dogs(sample=6)

    # Step 3: Initialize the Classification Skill
    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        client=OpenAI(),  # Add the client if you want to specify OpenAI explicitly
        categories=["cat", "dog"],
        max_categories=1,
        system_prompt="We want to classify images by what is in the picture.",
    )

    # Define which columns to treat as image data
    column_modalities = {"image_base64": "image_base64"}

    # Step 4: Prepare tasks from the test data
    tasks = skill.create_tasks(
        data,
        column_modalities=column_modalities
    )

    # Step 5: Execute classification tasks
    results = skill.run_tasks_in_parallel(tasks)

    # Step 6: Map results back to the test DataFrame
    print(results)

    # Step 7: Save the Skill configuration
    skill.save("MyCustomSkillIMG.json")


if __name__ == "__main__":
    main()