import os

from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import imdb_reviews_50k
import plotly.express as px

def main():
    # Step 1: Provide your OpenAI
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    # Step 2: Initialize the LearnSkill
    learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    # Step 3: Load sample data
    data = imdb_reviews_50k(sample=100)

    # Step 4: Learn the skill with the defined task
    skill = learner.learn_skill(
        data,
        task='Based on data sample define 3 thematic'
             ' categories satirical, quirky and absurd'
             ' Return category value on key "category"',
        model_name="gpt-4o-mini",
    )

    # Step 5: Prepare and execute classification tasks
    tasks = skill.create_tasks(data)
    results = skill.run_tasks_in_parallel(tasks)

    print(results)

if __name__ == "__main__":
    main()