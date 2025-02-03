from dotenv import load_dotenv
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import imdb_reviews_50k
load_dotenv()

def main():
    # Step 1: Provide your OpenAI

    # Step 2: Initialize the LearnSkill
    learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    # Step 4: Learn the skill with the defined task
    skill = learner.learn_skill(
        df=[],
        task='parse text input and select the most simmilar product to the query'
             'return structured prduct infromation for best product on key name, price (float), short_description',
        model_name="gpt-4o-mini",
    )

    # Step 5: Prepare and execute classification tasks
    skill.save('select_product.json')

if __name__ == "__main__":
    main()