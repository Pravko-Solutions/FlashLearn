from openai import OpenAI
import json
from flashlearn.skills.classification import ClassificationSkill
from flashlearn.utils import demo_data, imdb_reviews_50k


def main():
    # Step 1: Provide your OpenAI
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

    client = OpenAI()

    # Step 2: Load sample data (list of dicts with "review" and "sentiment" keys)
    reviews = imdb_reviews_50k(sample=100)

    # Step 3: Initialize the Classification Skill
    skill = ClassificationSkill(
        model_name="gpt-4o-mini",
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

    if False:
        # Step 5: We could upload tasks file to Batch API
        batch_file = client.files.create(
            file=open('tasks.jsonl', "rb"),
            purpose="batch"
        )
        batch_job = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )
        batch_job = client.batches.retrieve(batch_job.id)
        print(batch_job)
        print('You will need this id to pull: ' + str(batch_job.output_file_id))

        # AFTER 24h
        result_file_id = batch_job.output_file_id
        result = client.files.content(result_file_id).content

        result_file_name = "data/batch_job_results_movies.jsonl"

        with open(result_file_name, 'wb') as file:
            file.write(result)

        # Loading data from saved file
        results = []
        with open(result_file_name, 'r') as file:
            for line in file:
                # Parsing the JSON string into a dict and appending to the list of results
                json_object = json.loads(line.strip())
                results.append(json_object)
        # Reading only the first results

        for res in results:
            task_id = res['custom_id']
            # Getting index from task id
            index = task_id.split('-')[-1]
            result = res['response']['body']['choices'][0]['message']['content']
            review = reviews[int(index)]
            review['result'] = result

        with open('data_with_results.jsonl', 'w') as jsonl_file:
            for entry in results:
                jsonl_file.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    main()