from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import ClassifyDifficultyOfQuestion
from flashlearn.utils import imdb_reviews_50k


def main():
    # Step 1: Provide your OpenAI
    #os.environ["OPENAI_API_KEY"] = "API KEY"

    # Step 2: Load sample data
    reviews = imdb_reviews_50k(sample=50)

    # Step 3: Load the previously created ClassificationSkill
    skill = GeneralSkill.load_skill(ClassifyDifficultyOfQuestion)
    # Step 4: Build tasks from test data
    tasks = skill.create_tasks(reviews)
    # Step 5: Run tasks in real-time
    results = skill.run_tasks_in_parallel(tasks)
    print(results)


if __name__ == "__main__":
    main()