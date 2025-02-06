# Creating an Autonomous Research Assistant
<span style="color:red">This is red text</span>

---

## Step 0: Environment Setup

We import required libraries, load any environment variables (e.g., API keys from a .env file), and prepare a folder for JSON artifacts (optional).

### Environment Setup

Install the necessary packages:
- flashlearn (if you’d like to create tasks/skills)
- browser-use (for the browser agent)
- playwright (for controlling the browser, plus “playwright install” for setup)
- dotenv (for environment variables)
- openai or any other relevant LLM

```python
import os
import json
import asyncio
from dotenv import load_dotenv

# Use pip or conda to install these if needed:
# !pip install flashlearn browser-use playwright python-dotenv openai
# Then run once to install browsers if you haven't already:
# !playwright install

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Optional: create a folder to store JSON artifacts (skills, tasks, etc.)
json_folder = "json_artifacts"
os.makedirs(json_folder, exist_ok=True)

print("Step 0 complete: Environment ready.")
```

---

## Step 1: Example Data or Use Case

To illustrate how you might structure tasks, we create a small dataset or list of tasks that require searching the web for specific information.

### Define a Use Case or Example Data

Here, we imagine a scenario where authors or topics are provided, and we want more information from Google searches and subsequent website visits.

```python
# Example tasks: We want to learn about a set of topics
research_topics = [
    {"topic": "Browser-Use Python library"},
    {"topic": "OpenTelemetry best practices"},
    {"topic": "Latest news on quantum computing"}
]

print("Step 1 complete: Example research topics initialized.")
print("Sample topic:", research_topics[0])
```

---

## Step 2: Define a Skill for Query Generation

Sometimes you may want an LLM to transform your initial dataset (topics) into more precise search queries. With flashlearn, you can define a skill that, for each “topic,” produces a “query.” If you prefer to manually define queries, you can skip this step.

### Create and Store a Skill for Generating Queries

We can teach a model how to turn broad topics into a more targeted query phrase for Google.

```python
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.skills import GeneralSkill
from openai import OpenAI

def create_query_skill(data):
    """
    Defines a skill which transforms a 'topic' into a Google search query string.
    """
    client = OpenAI()  # Using openai
    learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    # For example, the instruction can ask the model to produce a succinct query
    instruction = (
        "For each 'topic', create a short, targeted Google search query. "
        "Output JSON with the key 'query'."
    )

    skill = learner.learn_skill(data, task=instruction, model_name="gpt-4o-mini")
    return skill

# Uncomment below to create, store, and reload examples of your skill
# skill_query = create_query_skill(research_topics)
# skill_json_path = os.path.join(json_folder, "research_query_skill.json")
# skill_query.save(skill_json_path)
# loaded_skill_query = GeneralSkill.load_skill(skill_json_path)
```

---

## Step 3: Create Research Tasks (Queries)

Here, we either manually create tasks or use our optional skill from the previous step. Each task is a dictionary specifying what the agent will search.

### Create Research Tasks

If you used a skill, you’d run it on “research_topics” to produce “query” strings. Otherwise, we can do it by hand.

```python
# For illustration, let's assume we've already generated specific queries:
research_tasks = [
    {"query": "Browser-Use Python library usage example"},
    {"query": "OpenTelemetry best practices in production environment"},
    {"query": "Recent breakthroughs in quantum computing, 2023"}
]

print("Step 3 complete: Research tasks ready.")
print("Sample task:", research_tasks[0])
```

---

## Step 4 (Optional): Save Tasks to JSONL

We can store these tasks in a JSONL file for reproducibility or auditing.

### Save Tasks to JSONL

This step is useful if you want to process them offline or share them with teammates.

```python
tasks_jsonl_path = os.path.join(json_folder, "research_tasks.jsonl")
with open(tasks_jsonl_path, 'w') as f:
    for task in research_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Step 4 complete: Tasks saved to {tasks_jsonl_path}")
```

---

## Step 5: Load Tasks from JSONL (Optional)

If needed, you can load tasks from the JSONL file. This helps keep your pipeline modular.

### Load Tasks from JSONL

Useful if you want to handle tasks across different notebooks or machines.

```python
loaded_research_tasks = []
with open(tasks_jsonl_path, 'r') as f:
    for line in f:
        loaded_research_tasks.append(json.loads(line))

print("Step 5 complete: Research tasks reloaded from JSONL.")
print("Sample reloaded task:", loaded_research_tasks[0])
```

---

## Step 6: Create the Browser Agent for Searching Google

We use browser-use’s Agent to navigate a browser session. In this example, we instruct the agent to go to Google, perform a search, click results, and gather content. We use concurrency to control how many we run in parallel.

### Create a Browser Agent Function and Parallel Execution

We define a function that uses the browser-use Agent to search Google for a query, explore the first relevant link, and return text. Then we run these agents in parallel or sequentially (as you'd like).

```python
from browser_use.agent.service import Agent
from langchain_openai import ChatOpenAI

async def google_browser_agent(query: str) -> str:
    """
    Agent that goes to Google, searches for 'query',
    clicks on the most relevant result, and returns the page text.
    """
    # We define a simple instruction for the Agent
    task_description = (
        f"Go to Google.com, search for '{query}', select the top relevant website, "
        "click on it, and return the textual content from that page."
    )
    agent = Agent(
        task=task_description,
        llm=ChatOpenAI(model="gpt-4o"),  # or your chosen LLM, e.g., 'gpt-4o'
    )
    result = await agent.run()

    # Typically, the final item in history includes the extracted page content
    page_text = result.history[-1].result[0].extracted_content
    return page_text

async def run_google_agents_in_parallel(tasks, concurrency: int = 2):
    """
    Runs up to 'concurrency' browser agents in parallel to execute each query.
    Returns a list of extracted texts, in the same order as 'tasks'.
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def limited(query):
        async with semaphore:
            return await google_browser_agent(query["query"])

    # Create a list of tasks (one per query)
    agent_tasks = [asyncio.create_task(limited(t)) for t in tasks]
    results = await asyncio.gather(*agent_tasks)
    return results
```

---

## Step 7: Run the Research Agents

Now we will run the tasks in parallel (or as configured) using asyncio, collecting the textual content from each visited result.

### Run the Research Agents

We pass our task list (which includes queries) to the asynchronous “run_google_agents_in_parallel” function, storing the results in a list you can map back to your original tasks.

```python
research_results = asyncio.run(run_google_agents_in_parallel(loaded_research_tasks, concurrency=1))

print("Step 7 complete: Research agent tasks finished.")
for i, content in enumerate(research_results):
    print(f"\n=== Result {i+1} for query '{loaded_research_tasks[i]['query']}' ===\n")
    print(content[:300], "...")  # print only a snippet
```

---

## Step 8: Map Results Back into Original Data

We integrate the returned texts into our original task structures, creating a combined record that has both the query and the scraped content.

### Integrate Results into Original Task Data

Attach the “page_text” or “scraped_content” to the corresponding task object for further processing or analysis.

```python
annotated_data = []
for idx, content in enumerate(research_results):
    item = loaded_research_tasks[idx]
    # Attach the content from the agent
    item["results_text"] = content
    annotated_data.append(item)

print("Step 8 complete: Data annotated with agent results.")
print(json.dumps(annotated_data[0], indent=2))
```

---

## Step 9 (Optional): Further Skills or Additional Processing

Now that you have raw text from each website, you can learn another skill (just like with queries) to summarize text, quote it etc:
- Summarization skill → to condense the text  
- Q&A skill → to answer specific questions about the content  
- Classification skill → to categorize or label the text  

This step is entirely up to your application needs.

### Use Additional Skills

For instance, you could create a summarization skill that processes “results_text” for each item and returns a short summary or bullet points.
---

## Step 10: Store Final Results

Finally, we can store the fully annotated dataset (topic, query, results_text, optional summary, etc.) in a JSON or JSONL file for downstream usage, auditing, or integration into broader pipelines.

### Final Storing of Research Results

We save the final dataset, now containing queries and extracted page text, as JSON. Further tasks or manual review can happen later.

```python
final_results_path = os.path.join(json_folder, "research_assistant_output.json")
with open(final_results_path, 'w') as f:
    json.dump(annotated_data, f, indent=2)

print(f"Step 10 complete: Final research results stored at {final_results_path}")
```

---

## Summary

Using the above steps, you can:

- Define your research tasks (queries or topics).  
- Optionally use AI “skills” to generate more queries, and checking loops to improve results.  
- Employ browser-use’s Agent to autonomously navigate Google (or another site), gather relevant webpage text, and return it.  
- Combine results into your data structure for subsequent analysis (summaries, classification, Q&A, etc.).  
- Store everything as JSON or JSONL to keep your workflow transparent, reproducible, and auditable.

With minimal changes, you can direct the agent to other sites, mimic multi-step navigation (e.g., logging in, clicking sub-links), and chain multiple skills for advanced data extraction or knowledge synthesis. This approach turns your code into a flexible, AI-driven, fully autonomous “research assistant.”

## Tips to improve

You can greatly improve results by:

- Generate more than 1 user query, up to N 
- Follow good links on child pages with results.  
- Generate and answer from the data -> Learn skill ANSWER
- You can chain results to get even more refined data
- Use infinite contex hack like here [Link](https://github.com/Pravko-Solutions/FlashLearn/blob/main/examples/deepseek_inifinite_context.py)
