from flashlearn.skills.classification import ClassificationSkill
from flashlearn.skills import DiscoverLabelsSkill
from flashlearn.utils import imdb_reviews_50k


def main():
    # Step 1: Provide your OpenAI
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    # Step 2: Load sample data
    data = imdb_reviews_50k(sample=100)

    # Step 3: Discover labels/clusters
    labeling_skill = DiscoverLabelsSkill(
        model_name="gpt-4o-mini",
        label_count=4,
        system_prompt="Uncover hidden themes in this movie reviews. Be funny",
    )
    labeling_skill.save()

    # Step 4: Create tasks for discovering labels
    tasks = labeling_skill.create_tasks(data)
    results_labels = labeling_skill.run_tasks_in_parallel(tasks)
    labels = results_labels['0']['labels']  # Extract discovered labels

    # Step 5: Create a classification skill with discovered labels
    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
        categories=labels,
        max_categories=1,
        system_prompt="We want to classify short movie reviews in listed categories",
    )

    # Step 6: Build classification tasks
    tasks = skill.create_tasks(data)

    # Step 7: Run tasks in real-time
    results = skill.run_tasks_in_parallel(tasks)
    print(results)

if __name__ == "__main__":
    main()