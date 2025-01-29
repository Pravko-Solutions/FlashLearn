import os
from openai import OpenAI
from flashlearn.skills.classification import ClassificationSkill


def super_simple_chunker(text, chunk_size=1000):
    """Chunks text into smaller segments of specified size."""
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return [{"text": chunk} for chunk in chunks]


def infinite_context(question, context):
    """
    Uses a language model to provide answers to a given question
    by processing a large context into relevant chunks.
    """
    # Step 1: Setup your provider

    # OpenAI setup - Uncomment if using OpenAI directly
    # model_name = "gpt-4o-mini"
    # client = OpenAI()
    # os.environ["OPENAI_API_KEY"] = 'Your api key'

    # DeepSeek setup
    model_name = 'deepseek-chat'
    client = OpenAI(
        api_key='YOUR DEEPSEEK API KEY',
        base_url="https://api.deepseek.com",
    )

    # Step 2: Chunk context like you would with any RAG flow
    chunks = super_simple_chunker(context)

    # Step 3: Initialize the Classification Skill - Classify relevant content
    skill = ClassificationSkill(
        model_name=model_name,
        client=client,
        categories=["relevant", "somehow_relevant", "irrelevant"],
        max_categories=1,
        system_prompt="Classify content based on relevancy to the task" f"{question}",
    )

    # Step 4: Prepare classification tasks (passing the list of dicts + columns to read)
    iterations = 0
    while len(chunks) > 64 or iterations > 2:
        tasks = skill.create_tasks(chunks)

        # Narrow down on quality context
        results = skill.run_tasks_in_parallel(tasks)
        print(results)

        # Step 6: Map results and reiterate if still too many chunks
        for i, review in enumerate(chunks):
            chunks[i]['category'] = results[str(i)]['categories']
        chunks = [{'text': review['text']} for review in chunks if review['category'] == 'relevant']

        iterations += 1

    # Answer
    answer = client.chat.completions.create(
        model=model_name,
        messages=[
            {'role': 'user', 'content': str(chunks)},
            {'role': 'user', 'content': question}
        ]
    )

    return answer.choices[0].message.content


if __name__ == "__main__":
    # Open the long context file
    file_path = 'context.txt'
    file = open(file_path, 'r', encoding='utf-8')

    # Read the file's contents
    file_contents = file.read()

    answer = infinite_context('YOUR QUESTION', file_contents)
    print(answer)