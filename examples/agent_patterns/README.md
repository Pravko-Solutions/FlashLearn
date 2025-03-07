# Is More Agents Better?

A demonstration of single-agent vs. multi-agent text classification pipelines on IMDB movie reviews.

## Overview

This project explores how adding more agents (or steps) to a classification pipeline affects accuracy. We train a basic sentiment classifier on IMDB data, then progressively insert additional “agents” to provide emotional summaries, emotional statements, and explanations. Finally, we compare how each step affects the final classification accuracy (i.e., determining whether a review is positive or negative).

The key takeaway? More agents does not necessarily mean better accuracy!

## Project Structure

1. **Skill Definitions**  
   - Located in the `definitions/` folder.  
   - Each JSON file (e.g., `classification.json`, `emotional_summary.json`, etc.) defines a “skill” learned by the flashlearn library (e.g., how to classify sentiment, summarize emotions, or extract statements).

2. **Pipelines**  
   - We implement four progressively more complex pipelines in standalone scripts:  
     1. `classification_only.py`  
        - No intermediate steps — the classifier alone decides the sentiment.  
     2. `summary_then_classification.py`  
        - Runs the “emotional_summary” agent, then feeds that summary into the classifier.  
     3. `summary_statements_then_classification.py`  
        - Executes “emotional_summary” → “emotional_statements” → classification.  
     4. `summary_statements_explanation_then_classification.py`  
        - The most elaborate pipeline: “emotional_summary” → “emotional_statements” → “explanation” → classification.

3. **IMDB Dataset**  
   - We rely on the flashlearn utility `imdb_reviews_50k` to read a subset of the IMDB movie reviews dataset. Each record includes:  
     - `text`: The movie review text.  
     - `sentiment`: The true label (`"positive"` or `"negative"`).

4. **Accuracy Comparison**  
   - Each pipeline removes the `sentiment` field before classification. After predictions, we compare them to the hidden ground truth.

## Results

Below is a table summarizing the final accuracy of each pipeline on a full sample:

| Pipeline Approach                                            | Accuracy |
|-------------------------------------------------------------|----------|
| Step 1: Classification-Only                                 | 0.95     |
| Step 2: Summary → Classification                            | 0.94     |
| Step 3: Summary → Statements → Classification               | 0.93     |
| Step 4: Summary → Statements → Explanation → Classification | 0.94     |

**Key Insight**: While more intermediate agents can offer additional analysis, context, or interpretability, they don’t necessarily improve raw sentiment accuracy. In fact, the single-agent approach (Step 1) achieved the highest accuracy.

## Usage

1. **Install Requirements**  
   - Ensure you have Python 3.8+ and the [flashlearn](https://github.com/flashlearn-xyz/flashlearn) library (or similar) installed.  
   - Example:  
     ```bash
     pip install flashlearn
     ```

2. **Prepare Skill Definitions**  
   - Make sure `classification.json`, `emotional_summary.json`, `emotional_statements.json`, and `explanation.json` are in the `definitions/` folder.

3. **Run Pipelines**  
   - Classification only:  
     ```bash
     python classification_only.py
     ```  
   - Summary → Classification:  
     ```bash
     python summary_then_classification.py
     ```  
   - Summary → Statements → Classification:  
     ```bash
     python summary_statements_then_classification.py
     ```  
   - Summary → Statements → Explanation → Classification:  
     ```bash
     python summary_statements_explanation_then_classification.py
     ```

4. **Observe Accuracy**  
   - Each script prints out predicted labels alongside the actual (hidden) sentiment and computes a final accuracy percentage.

## Project Takeaways

1. **Simplicity Can Win**  
   - The single-step pipeline performed best (95% accuracy).  
   - Multi-step approaches can sometimes introduce abstraction or partial misinterpretation of text.

2. **Modular Insights**  
   - Adding “emotional_summary,” “emotional_statements,” or “explanation” agents can be valuable if you need deeper insights, interpretability, or advanced data constructs.  

3. **Context Matters**  
   - Different datasets or tasks might benefit more from extra agents—no one-size-fits-all solution.

## Contributing

- Feel free to open PRs or issues if you discover improvements or new ways to chain multiple agents while preserving or boosting accuracy.

## License

This project is provided “as is,” with no warranty. Refer to the accompanying license file (if provided) or use it under the terms of your choice.

---

**Is More Agents Better?**  
In short, not always. While multi-agent pipelines offer richer insights, maximum classification accuracy is sometimes easier to achieve with a single, carefully trained agent!