import os
from openai import OpenAI
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import ConvertToGoogleQueries, SimpleGoogleSearch

os.environ["OPENAI_API_KEY"]  = ""
GOOGLE_API_KEY = ""
GOOGLE_CSE_ID = ""
MODEL_NAME = "gpt-4o-mini"

question = 'When was python launched?'
client = OpenAI()
skill = GeneralSkill.load_skill(ConvertToGoogleQueries, client=client)
queries = skill.run_tasks_in_parallel(skill.create_tasks([{"query": question}]))["0"]
results = SimpleGoogleSearch(GOOGLE_API_KEY, GOOGLE_CSE_ID).search(queries['google_queries'])
msgs = [
    {"role": "system", "content": "insert links from search results in response to quote it"},
    {"role": "user", "content": str(results)},
    {"role": "user", "content": question},
]
print(client.chat.completions.create(model=MODEL_NAME, messages=msgs).choices[0].message.content)