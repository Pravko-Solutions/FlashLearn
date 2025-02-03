import os

from dotenv import load_dotenv
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import imdb_reviews_50k
load_dotenv()

def main():
    # Step 1: Provide your OpenAI key in .env file
    # Step 2: Initialize the LearnSkill
    learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    # Step 4: Learn the skill with the defined task
    skill = learner.learn_skill(
        df=[],
        task='from input create one google query called on key query',
        model_name="gpt-4o-mini",
    )

    # Step 5: Prepare and execute classification tasks
    skill.save('make_query.json')

if __name__ == "__main__":
    main()