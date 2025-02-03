# Browser Price Matching Tool

This project helps you adjust your product prices by comparing them to similar products available in the market. It uses a browser agent to search for products (e.g., on Amazon) and leverages custom "skills" to generate effective search queries and structure web data into a standard format. The enriched data can then be used to update your product prices.

---

## File Structure

- **learn_skill.py**  
  Learns a new skill for creating clear and effective product search queries using the FlashLearn library and OpenAI’s GPT-4o-mini model.

- **learn_skill_select_best_product.py**  
  Learns a skill to parse browser response text and select the best matching product along with its key details (name, price, short description).

- **make_query.json**  
  Contains the generated skill definition for producing search queries from product names. This file is produced by running `learn_skill.py`.

- **select_product.json**  
  Contains the generated skill definition for parsing search results and selecting the best product. This file is produced by running `learn_skill_select_best_product.py`.

- **product_price_matching.py**  
  The main pipeline that:
  - Reads product data (from CSV or demo list).
  - Uses the skill in `make_query.json` to generate clean search queries.
  - Launches asynchronous browser agents to search on Amazon.
  - Structures the scraped web data.
  - Uses the skill in `select_product.json` to extract the best matching product details.
  - Enriches and prints the final product data.

---

## Installation & Setup

### Requirements

- Python 3.7 or later
- Required Python packages:
  - `python-dotenv`
  - `openai`
  - `langchain_openai`
  - `flashlearn`
  - `requests`
  - `pytest-playwright`

### Steps

1. **Install Python dependencies:**

   ```bash
   pip install python-dotenv openai langchain_openai flashlearn requests pytest-playwright
   ```

2. **Install the required browsers for Playwright:**

   ```bash
   playwright install
   ```

3. **Set up your OpenAI API Key:**

   Create a `.env` file in the project directory and add the following line:

   ```env
   OPENAI_API_KEY="sk-your_api_key_here"
   ```

---

## Process Overview

1. **Learn Skill for Query Creation:**

   - Run `learn_skill.py`.
   - This script trains a skill that generates clean, Google-like search queries from your product names.
   - The resulting skill definition is saved as `make_query.json`.

2. **Learn Skill for Selecting the Best Product:**

   - Run `learn_skill_select_best_product.py`.
   - This script trains a skill to parse browser results and select the best matching product based on details like name, price, and a brief description.
   - The resulting skill definition is saved as `select_product.json`.

3. **Run the Price Matching Pipeline:**

   - Run `product_price_matching.py`.
   - The script performs the following steps:
     - Loads your product data (for demonstration, a list of product dictionaries is used; in production, you can modify this to load a CSV file).
     - Generates search queries using the `make_query.json` skill.
     - Starts asynchronous browser agents to search on Amazon using the generated queries.
     - Scrapes and structures the website data.
     - Uses the `select_product.json` skill to pick the best matching product.
     - Enriches the original product data with the new information and prints the results.

---

## Customization

- **Concurrency:**  
  Adjust the number of parallel browser agents by modifying the `concurrency` parameter in `product_price_matching.py`.

- **Product Data:**  
  Replace the demo product list with your CSV input or other data sources as needed.

- **Skill Adjustments:**  
  Feel free to extend or modify the skill definitions if your query generation or data extraction requirements change.

---

## Troubleshooting

- Ensure the `.env` file is correctly set up with your valid OpenAI API key.
- Verify that all required packages are installed.
- Check output logs (with verbose mode enabled) for any issues during skill training or pipeline execution.
- Confirm that the browsers required by Playwright are correctly installed by running `playwright install`.

---

## Conclusion

The Browser Price Matching Tool automates the process of pricing analysis by:
- Generating effective search queries.
- Running browser agents to capture real-time product data.
- Structuring and enriching your product data with relevant market information.

This tool minimizes manual intervention while providing you with up-to-date market insights to help you adjust your product prices effectively.
