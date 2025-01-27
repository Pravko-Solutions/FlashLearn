import json
import os

from openai import OpenAI

from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import imdb_reviews_50k


def main():
    # Step 1: Setup your provider
    #os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    # Deepseek client
    #OpenAI(
        #api_key='YOUR DEEPSEEK API KEY',
        #base_url="https://api.deepseek.com",
    #)
    # Step 2: Load sample data (list of dicts with "review" and "sentiment" keys)
    reviews = imdb_reviews_50k(sample=100)

    # Step 3: Initialize the Classification Skill
    skill = ClassificationSkill(
        #model_name="deepseek-chat",
        model_name="gpt-4o-mini",
        client=OpenAI(),
        categories=["positive", "negative"],
        max_categories=1,
        system_prompt="We want to classify short movie reviews by sentiment."
    )
    # Step 4: Prepare classification tasks (passing the list of dicts + columns to read)
    removed_sentiment = [{'review': x['review']} for x in reviews]
    tasks = skill.create_tasks(removed_sentiment)
    # Step 7: Save results to a JSONL file
    with open('tasks.jsonl', 'w') as jsonl_file:
        for entry in tasks:
            jsonl_file.write(json.dumps(entry) + '\n')


    # Step 5: Execute classification tasks in real time ( We could upload file to Batch api)
    # We are using OpenAI tier 5 limits
    results = skill.run_tasks_in_parallel(tasks)

    # Step 6: Map results and check accuracy

    correct = 0
    for i, review in enumerate(reviews):
        reviews[i]['category'] = results[str(i)]['categories']
        if reviews[i]['sentiment'] == results[str(i)]['categories']:
            correct += 1
    print(f'Accuracy: {round(correct / len(reviews), 2)} %')

    # Step 7: Save results to a JSONL file
    with open('results.jsonl', 'w') as jsonl_file:
        for entry in reviews:
            jsonl_file.write(json.dumps(entry) + '\n')

    # Step 8: Save the Skill configuration
    skill.save("BinaryClassificationSkill.json")



if __name__ == "__main__":
    main()