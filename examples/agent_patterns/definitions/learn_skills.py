import os
import json

import dotenv
from flashlearn.skills.learn_skill import LearnSkill
from flashlearn.utils import imdb_reviews_50k
dotenv.load_dotenv()
def main():
    # (Optional) Provide your API key, if required
    # os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

    # --------------------------------------------------------------------------
    # STEP 1: Load IMDB data and REMOVE the existing sentiment label from each record
    # --------------------------------------------------------------------------
    data = imdb_reviews_50k(sample=20)  # small sample for demonstration
    # Save original sentiment in a separate field, then remove it

    # NOTE: We'll use this same data to learn all needed skills.
    # Usually you’d separate training and test sets, but for simplicity we
    # reuse the same “data” to define tasks (the library is demonstration-based).

    # --------------------------------------------------------------------------
    # STEP 2: Define a single agent skill (no reflection/multi-step)
    # --------------------------------------------------------------------------
    single_learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    single_task_prompt = (
        "You are a basic sentiment classifier. Return JSON with key 'label' "
        "which is strictly 'positive' or 'negative'."
    )

    single_skill = single_learner.learn_skill(
        data,
        task=single_task_prompt,
        model_name="gpt-4o-mini"
    )

    single_skill_path = "classification.json"
    single_skill.save(single_skill_path)
    print(f"Saved Single-Agent classification.json")

    # --------------------------------------------------------------------------
    # STEP 3: Define Reflection-based approach with TWO agents (two separate skills)
    #    a) Agent A: “First guess”
    #    b) Agent B: “If there's doubt, revise classification”
    # --------------------------------------------------------------------------
    reflection_learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)
    reflection_prompt_A = (
        "You are a sentiment summarizer and you summarize emotions in the text"
        "Output JSON with a key 'emotional_summary' set"
    )
    skill_reflection_A = reflection_learner.learn_skill(
        data, task=reflection_prompt_A, model_name="gpt-4o-mini"
    )
    skill_reflection_A.save("emotional_summary.json")
    print("Saved Reflection emotional_summary.json")

    reflection_prompt_B = (
        "YOu make extract key emotional statements from the text"
        "Finally, return JSON with key 'emotional_statements'"
        "Where you list all emotional statements."
    )
    # We can reuse the same reflection_learner or a new one
    skill_reflection_B = reflection_learner.learn_skill(
        data, task=reflection_prompt_B, model_name="gpt-4o-mini"
    )
    skill_reflection_B.save("emotional_statements.json")
    print("Saved emotional_statements skill")

    # --------------------------------------------------------------------------
    # STEP 4: Multi-Agent Approach that BUILDS on reflection but adds an extra step
    #    e.g., A third agent or aggregator that merges final decisions or appends an explanation
    # --------------------------------------------------------------------------
    multi_learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    # Example aggregator: merges A & B or clarifies the final sentiment
    # In a real pipeline, you might pass Agent A + B outputs to this aggregator.
    multi_prompt = (
        "You provide explanation why you think this review is positive or negative on key explanation."
    )
    skill_multi_agent = multi_learner.learn_skill(
        data, task=multi_prompt, model_name="gpt-4o-mini"
    )
    skill_multi_agent.save("explanation.json")
    print("Saved explanation.json")

    print("All skills learned and saved!")

if __name__ == "__main__":
    main()