import os

from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import cats_and_dogs
import plotly.express as px

def main():
    # Step 1: Provide your OpenAI
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    # Step 2: Initialize the LearnSkill
    learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    # Step 3: Load sample image data
    data = cats_and_dogs(sample=10)

    # Step 4: Learn the skill from images
    column_modalities = {"image_base64": "image_base64"}
    skill = learner.learn_skill(
        data[:3],
        task='Based on data sample define 4 thematic funny categories'
             ' Return category value on key "category"',
        columns=['image_base64'],
        model_name="gpt-4o-mini",
        column_modalities=column_modalities
    )

    # Step 5: Prepare and execute classification tasks
    tasks = skill.create_tasks(data[3:], columns=['image_base64'], column_modalities=column_modalities)
    results = skill.run_tasks_in_parallel(tasks)

    # Step 6: Map results back to the test DataFrame
    print(results)
if __name__ == "__main__":
    main()