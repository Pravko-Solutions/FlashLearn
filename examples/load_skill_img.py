import json
import os

from flashlearn.skills import GeneralSkill
from flashlearn.utils import cats_and_dogs


def main():
    # Step 1: Provide your OpenAI
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    # Step 2: Load sample image data
    pictures = cats_and_dogs(sample=6)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'MyCustomSkillIMG.json')
    # Step 3: Load the previously created skill for images
    with open(file_path, "r") as file:
        data = json.load(file)
    skill = GeneralSkill.load_skill(data)

    # Step 4: Build tasks from test data
    column_modalities = {"image_base64": "image_base64"}
    tasks = skill.create_tasks(pictures, column_modalities=column_modalities)

    # Step 5: Run tasks in real-time
    results = skill.run_tasks_in_parallel(tasks)

    # Step 6: Map results to df_test
    print(results)

if __name__ == "__main__":
    main()