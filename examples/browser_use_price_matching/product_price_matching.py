import os
import json
import asyncio
import requests

from dotenv import load_dotenv
from openai import OpenAI
from flashlearn.skills import GeneralSkill
from browser_use.agent.service import Agent
from langchain_openai import ChatOpenAI

# Make .env file and OPENAI_API_KEY  = "sk-proj......."
load_dotenv()


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
MODEL_NAME = "gpt-4o-mini"


# ------------------------------------------------------------------------------
# Data
# ------------------------------------------------------------------------------
products = [
    {"product_name": "Apple iPhone14! "},
    {"product_name": " Samsung Galaxy-S23"},
    {"product_name": "Sony_WH-1000XM4_Headphones"},
    {"product_name": "Nintendo Switch"},
    {"product_name": "Dyson! V11!! VacuumCleaner "},
    {"product_name": "Dell XPS13~Laptop"},
    {"product_name": "Google Nest Thermo!stat"},
    {"product_name": "Tesla Model#S"},
    {"product_name": " LG OLED-TV"},
    {"product_name": "AirWave~Ultrasonic#Humidifier"},
    {"product_name": "ZapMagic_Cleaning*Gel"},
    {"product_name": "NeoBlend!!Coffee Maker"},
    {"product_name": " BlueShade Sunglasses "},
    {"product_name": "AquaBoost Water!!Bottle#"},
    {"product_name": "PocketPro~~~Multi-tool"},
]
# For demo purposes, limit to the first 3 products
products = products[:5]


# ------------------------------------------------------------------------------
# Asynchronous Functions
# ------------------------------------------------------------------------------
async def browser_agent(query: str) -> str:
    """
    A single agent that goes to Amazon, searches for the given 'query',
    clicks on the most similar product, and returns the page text.
    """
    agent = Agent(
        task=f"Go to Amazon.com, search for {query}, click on the most similar product and return page text",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()

    # Extract the text from the final item in the agent's history
    product_data = result.history[-1].result[0].extracted_content
    return product_data


async def run_browser_agents_in_parallel(queries, concurrency: int = 5) -> list:
    """
    Spawns up to 'concurrency' browser agents in parallel to handle queries.

    Args:
        queries (list[str]): A list of query strings to search on Amazon.
        concurrency (int): The maximum number of parallel tasks.

    Returns:
        list of str: The extracted content returned by each browser agent.
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def limited_browser_agent(q):
        async with semaphore:
            return await browser_agent(q["query"])

    tasks = [asyncio.create_task(limited_browser_agent(q)) for q in queries]

    # gather results in the same order as tasks
    results = await asyncio.gather(*tasks)
    return results


# ------------------------------------------------------------------------------
# Main Logic
# ------------------------------------------------------------------------------
def main():
    # Initialize OpenAI client
    client = OpenAI()

    # --------------------------------------------------------------------------
    # Read skill definitions from JSON files
    # --------------------------------------------------------------------------
    with open("make_query.json", "r") as file:
        skill_definition_query = json.load(file)

    with open("select_product.json", "r") as file:
        skill_definition_best_product = json.load(file)

    # --------------------------------------------------------------------------
    # 1) Create queries from products
    # --------------------------------------------------------------------------
    skill = GeneralSkill.load_skill(skill_definition_query, client=client)
    tasks = skill.create_tasks(products)
    queries_by_index = skill.run_tasks_in_parallel(tasks)
    # queries_by_index is typically a dict with integer keys and query dict values

    # --------------------------------------------------------------------------
    # 2) Search on Amazon using parallel browser agents
    # --------------------------------------------------------------------------
    # Convert the dict to a list to keep track of original indices
    queries_list = [queries_by_index[str(i)] for i in range(len(queries_by_index))]

    # Run up to N browser agents in parallel
    results_texts = asyncio.run(run_browser_agents_in_parallel(queries_list, concurrency=1))

    # Update products with the results text
    for idx, text in enumerate(results_texts):
        products[idx].update({
            "query": queries_list[idx]["query"],
            "results_text": str(text),
        })

    # --------------------------------------------------------------------------
    # 3) Select best match using a second skill
    # --------------------------------------------------------------------------
    skill_best = GeneralSkill.load_skill(skill_definition_best_product, client=client)
    best_tasks = skill_best.create_tasks(products)
    best_products = skill_best.run_tasks_in_parallel(best_tasks)

    # Update products with the best product match
    for idx, best_match in best_products.items():
        products[int(idx)].update({"best_product": best_match})

    # --------------------------------------------------------------------------
    # 4) Print final results
    # --------------------------------------------------------------------------
    print(json.dumps(products, indent=4))


# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()