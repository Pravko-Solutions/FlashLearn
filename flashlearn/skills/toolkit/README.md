# FlashLearn Toolkit – Task Reference

Welcome to the FlashLearn “toolkit” reference! Below you’ll find documentation for each built-in task, organized by category. Each task is defined with:

- A short description of its purpose.  
- The required JSON output schema to expect.  
- A minimal usage example with FlashLearn in Python.

All outputs from these tasks will be strict JSON following the specified schema.

---

## Usage Overview

To use any of these tasks:

```python
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import <TaskName>

skill = GeneralSkill.load_skill(<TaskName>)
tasks = skill.create_tasks([{"text": "Your input text here..."}])
results = skill.run_tasks_in_parallel(tasks)

print(results)
```

- Replace `<TaskName>` with the desired task (e.g., `SummarizeText`).
- The result will be a dictionary, keyed by task ID (e.g., `"0"`, `"1"`), containing valid JSON fields as described below.

---

# 1) Summarization & Rewriting (36 Tasks)

### 1. SummarizeText
- **Description**: Produce a concise summary (2–5 sentences) highlighting main points.  
- **JSON Output**:  
  ```json
  {
    "summary": "..."
  }
  ```

### 2. BulletPointSummary
- **Description**: Convert text into bullet points capturing main ideas.  
- **JSON Output**:  
  ```json
  {
    "bullet_points": ["point1", "point2", ...]
  }
  ```

### 3. HighlightKeyPoints
- **Description**: Extract key ideas or points from the text.  
- **JSON Output**:  
  ```json
  {
    "key_points": ["...", "..."]
  }
  ```

### 4. ParagraphReduction
- **Description**: Condense a paragraph by a given reduction factor.  
- **JSON Output**:  
  ```json
  {
    "reduced_paragraph": "..."
  }
  ```

### 5. RewriteInFormalTone
- **Description**: Rewrite text in a formal, academic style.  
- **JSON Output**:  
  ```json
  {
    "formal_text": "..."
  }
  ```

### 6. RewriteForChildren
- **Description**: Adapt text for a younger reading audience.  
- **JSON Output**:  
  ```json
  {
    "child_friendly": "..."
  }
  ```

### 7. SummaryWithQuotes
- **Description**: Summarize text but retain a few verbatim quotes.  
- **JSON Output**:  
  ```json
  {
    "summary": "..."
  }
  ```

### 8. MultiLanguageSummary
- **Description**: Give short summaries in multiple languages.  
- **JSON Output** (example):  
  ```json
  {
    "en": "...",
    "es": "...",
    "fr": "..."
  }
  ```

### 9. HeadlineGenerator
- **Description**: Generate a single catchy headline from the text.  
- **JSON Output**:  
  ```json
  {
    "headline": "..."
  }
  ```

### 10. BulletedSynopsis
- **Description**: Summarize text into bullet points with a custom bullet prefix.  
- **JSON Output**:  
  ```json
  {
    "synopsis_bullets": ["...", "..."]
  }
  ```

### 11. RewritePassiveToActive
- **Description**: Convert sentences from passive to active voice.  
- **JSON Output**:  
  ```json
  {
    "active_voice_text": "..."
  }
  ```

### 12. MultiParagraphSummary
- **Description**: Summarize into a specified number of paragraphs.  
- **JSON Output**:  
  ```json
  {
    "paragraphs": ["paragraph1", "paragraph2", ...]
  }
  ```

### 13. ThematicSummary
- **Description**: Provide short summaries of each theme in a provided list.  
- **JSON Output**:  
  ```json
  {
    "theme1": "...",
    "theme2": "...",
    ...
  }
  ```

### 14. ExecutiveBrief
- **Description**: Condense text into a concise executive summary.  
- **JSON Output**:  
  ```json
  {
    "executive_summary": "..."
  }
  ```

### 15. RewriteInQnAFormat
- **Description**: Transform text into a Q&A pair format.  
- **JSON Output**:  
  ```json
  {
    "qa_pairs": [
      ["Q1", "A1"],
      ["Q2", "A2"]
    ]
  }
  ```

### 16. RewriteAsPressRelease
- **Description**: Turn text into a formal press release style.  
- **JSON Output**:  
  ```json
  {
    "press_release": "..."
  }
  ```

### 17. HighlightActionItems
- **Description**: Extract action items or tasks from text (e.g. meeting notes).  
- **JSON Output**:  
  ```json
  {
    "action_items": ["...", "..."]
  }
  ```

### 18. SimplifyForNonExperts
- **Description**: Rewrite technical text in simple, plain language.  
- **JSON Output**:  
  ```json
  {
    "simple_explanation": "..."
  }
  ```

### 19. AcademicAbstract
- **Description**: Create an academic-style abstract summarizing the text.  
- **JSON Output**:  
  ```json
  {
    "abstract": "..."
  }
  ```

### 20. HighlightAndExpand
- **Description**: Identify crucial lines and provide expansions/definitions.  
- **JSON Output**:  
  ```json
  {
    "highlights": [
      {
        "text": "...",
        "expansion": "..."
      }
    ]
  }
  ```

### 21. RewriteSentencesAsBulletPoints
- **Description**: Turn each sentence into a bullet point.  
- **JSON Output**:  
  ```json
  {
    "bullets": ["...", "..."]
  }
  ```

### 22. SummarizeDialogue
- **Description**: Summarize a conversation or transcript into major points.  
- **JSON Output**:  
  ```json
  {
    "dialogue_summary": "..."
  }
  ```

### 23. StoryToFactSheet
- **Description**: Extract factual data from a narrative and map it to labeled fields.  
- **JSON Output**:  
  ```json
  {
    "facts": {
      "location": "...",
      "characters": "...",
      ...
    }
  }
  ```

### 24. ExtractImportantFigures
- **Description**: Extract numbers, stats, or key facts from the text.  
- **JSON Output**:  
  ```json
  {
    "figures": ["...", "..."]
  }
  ```

### 25. CreateShortDescription
- **Description**: Produce a concise promo/meta description from text.  
- **JSON Output**:  
  ```json
  {
    "short_description": "..."
  }
  ```

### 26. RewriteLegaleseInPlainLanguage
- **Description**: Convert “legalese” text into plain-language statements.  
- **JSON Output**:  
  ```json
  {
    "plain_language": "..."
  }
  ```

### 27. CreateSloganVersion
- **Description**: Generate a one-liner slogan from the text.  
- **JSON Output**:  
  ```json
  {
    "slogan": "..."
  }
  ```

### 28. RewriteInThirdPerson
- **Description**: Convert first-person references to third-person.  
- **JSON Output**:  
  ```json
  {
    "third_person_text": "..."
  }
  ```

### 29. RewordForPositiveTone
- **Description**: Make phrasing more positive or uplifting.  
- **JSON Output**:  
  ```json
  {
    "positive_version": "..."
  }
  ```

### 30. MultiSectionSummary
- **Description**: Break text into sections and summarize each.  
- **JSON Output**:  
  ```json
  {
    "sections": {
      "title1": "...",
      "title2": "...",
      ...
    }
  }
  ```

### 31. RewriteWithAdditionalContext
- **Description**: Insert extra contextual information into the text.  
- **JSON Output**:  
  ```json
  {
    "augmented_text": "..."
  }
  ```

### 32. ShortParagraphSynopsis
- **Description**: Create a single-sentence summary of a larger paragraph.  
- **JSON Output**:  
  ```json
  {
    "synopsis": "..."
  }
  ```

### 33. RewriteIntoBlogIntroduction
- **Description**: Turn a piece of text into a blog-style introduction.  
- **JSON Output**:  
  ```json
  {
    "blog_intro": "..."
  }
  ```

### 34. HighlightSafetyWarnings
- **Description**: Extract disclaimers or safety warnings from text.  
- **JSON Output**:  
  ```json
  {
    "warnings": ["...", "..."]
  }
  ```

### 35. RewriteAsStory
- **Description**: Transform text into a short narrative with specific characters.  
- **JSON Output**:  
  ```json
  {
    "story": "..."
  }
  ```

### 36. GenerateTableOfContents
- **Description**: Create a conceptual table of contents for the text by topic.  
- **JSON Output**:  
  ```json
  {
    "table_of_contents": ["...", "..."]
  }
  ```

---

# 2) Classification & Labeling (36 Tasks)

### 1. ClassifyReviewSentiment
- **Description**: Label each review as `"positive"`, `"negative"`, or `"neutral"`.  
- **JSON Output**:  
  ```json
  {
    "sentiment": "positive"
  }
  ```

### 2. DetectSpamMessage
- **Description**: Check if a message is spam (boolean).  
- **JSON Output**:  
  ```json
  {
    "is_spam": true
  }
  ```
  or
  ```json
  {
    "is_spam": false
  }
  ```

### 3. LanguageOfText
- **Description**: Identify the language of the input text.  
- **JSON Output**:  
  ```json
  {
    "language": "English"
  }
  ```

### 4. CategorizeNewsArticle
- **Description**: Classify a news article into a broad category like `"sports"`, `"politics"`, etc.  
- **JSON Output**:  
  ```json
  {
    "category": "sports"
  }
  ```

### 5. LabelTechSupportTickets
- **Description**: Classify support tickets by urgency (e.g., `"low"`, `"medium"`, `"high"`).  
- **JSON Output**:  
  ```json
  {
    "urgency": "high"
  }
  ```

### 6. TopicModelingSnippet
- **Description**: Identify possible topics or themes in a snippet.  
- **JSON Output**:  
  ```json
  {
    "topics": ["...", "..."]
  }
  ```

### 7. EmotionalToneDetection
- **Description**: Provide intensity scores (0–1) for emotions like joy, anger, sadness.  
- **JSON Output** (example):  
  ```json
  {
    "joy": 0.8,
    "anger": 0.2,
    "sadness": 0.1
  }
  ```

### 8. DomainSpecificClassification
- **Description**: Use a given domain context to refine classification.  
- **JSON Output**:  
  ```json
  {
    "classification": "medical"
  }
  ```

### 9. ClassifyCodeSnippetLanguage
- **Description**: Detect the programming language of a code snippet.  
- **JSON Output**:  
  ```json
  {
    "language": "Python"
  }
  ```

### 10. BrandMentionDetector
- **Description**: Detect brand references from a brand list.  
- **JSON Output** (example):  
  ```json
  {
    "BrandA": true,
    "BrandB": false,
    "BrandC": true
  }
  ```

### 11. IdentifyControversialContent
- **Description**: Label if content is potentially sensitive or controversial.  
- **JSON Output**:  
  ```json
  {
    "controversial": true
  }
  ```
  or
  ```json
  {
    "controversial": false
  }
  ```

### 12. CategoryPredictionFromKeywords
- **Description**: Match text to a predefined set of categories using keywords.  
- **JSON Output**:  
  ```json
  {
    "category": "..."
  }
  ```

### 13. ClassifyQualityOfWriting
- **Description**: Label the writing as `"excellent"`, `"good"`, or `"needs work"`.  
- **JSON Output**:  
  ```json
  {
    "quality": "excellent"
  }
  ```

### 14. SeriousnessOfComplaint
- **Description**: Rank a complaint from `"minor"` to `"major"`.  
- **JSON Output**:  
  ```json
  {
    "severity": "major"
  }
  ```

### 15. MusicGenreClassification
- **Description**: Predict the music genre from descriptive text.  
- **JSON Output**:  
  ```json
  {
    "music_genre": "rock"
  }
  ```

### 16. ImageCaptionsToSceneCategory
- **Description**: Classify an image caption (e.g., `"indoors"`, `"outdoors"`).  
- **JSON Output**:  
  ```json
  {
    "scene_category": "indoors"
  }
  ```

### 17. ClassifyCommentSection
- **Description**: Classify multiple user comments as `"toxic"`, `"spam"`, etc.  
- **JSON Output**:  
  ```json
  {
    "comment_labels": ["toxic", "spam", "relevant"]
  }
  ```

### 18. ClassifyLegalDocumentType
- **Description**: Identify the type of a legal document (`"contract"`, etc.).  
- **JSON Output**:  
  ```json
  {
    "legal_type": "will"
  }
  ```

### 19. LocationCategorySnippet
- **Description**: Classify a snippet about a place (e.g., `"tourist spot"`, `"historical site"`).  
- **JSON Output**:  
  ```json
  {
    "location_type": "tourist spot"
  }
  ```

### 20. TimelineEventClassifier
- **Description**: Tag an event description into a timeline category (`"political"`, `"social"`, etc.).  
- **JSON Output**:  
  ```json
  {
    "event_category": "political"
  }
  ```

### 21. SkillLevelAssessment
- **Description**: Classify skill level (`"beginner"`, `"intermediate"`, `"expert"`).  
- **JSON Output**:  
  ```json
  {
    "skill_level": "expert"
  }
  ```

### 22. ClassifyGenreOfBlurb
- **Description**: Tag a short text as `"romance"`, `"mystery"`, `"sci-fi"`, etc.  
- **JSON Output**:  
  ```json
  {
    "genre": "mystery"
  }
  ```

### 23. JobPostClassification
- **Description**: Label a job posting by field (`"IT"`, `"HR"`, `"marketing"`, etc.).  
- **JSON Output**:  
  ```json
  {
    "field": "IT"
  }
  ```

### 24. IdentifyHealthyVsUnhealthyRecipe
- **Description**: Decide if a recipe is generally healthy or unhealthy.  
- **JSON Output**:  
  ```json
  {
    "healthiness": "healthy"
  }
  ```
  or
  ```json
  {
    "healthiness": "unhealthy"
  }
  ```

### 25. LabelSarcasmInTweet
- **Description**: Detect sarcastic tweets.  
- **JSON Output**:  
  ```json
  {
    "sarcastic": true
  }
  ```
  or
  ```json
  {
    "sarcastic": false
  }
  ```

### 26. SkillBasedRoutingHandler
- **Description**: Classify a support case to route to the correct specialized agent.  
- **JSON Output**:
  ```json
  {
    "route_to": "billing_team"
  }
  ```

### 27. ClothingItemClassifier
- **Description**: Tag an item description as `"shirt"`, `"pants"`, `"shoes"`, etc.  
- **JSON Output**:  
  ```json
  {
    "clothing_type": "shoes"
  }
  ```

### 28. ProfanityFilter
- **Description**: Flag if text contains strong profanity.  
- **JSON Output**:  
  ```json
  {
    "contains_profanity": true
  }
  ```
  or
  ```json
  {
    "contains_profanity": false
  }
  ```

### 29. ClassifyMarketingHeadline
- **Description**: Label a marketing headline’s style (e.g., `"discount-based"`, `"emotional"`, `"urgency"`).  
- **JSON Output**:  
  ```json
  {
    "headline_style": "emotional"
  }
  ```

### 30. ProductReviewSatisfactionLevel
- **Description**: Classify satisfaction as `"low"`, `"medium"`, or `"high"`.  
- **JSON Output**:
  ```json
  {
    "satisfaction": "high"
  }
  ```

### 31. UserMoodAnalysis
- **Description**: Label a user’s mood (`"excited"`, `"frustrated"`, etc.).  
- **JSON Output**:
  ```json
  {
    "mood": "frustrated"
  }
  ```

### 32. ShortAnswerGradedEvaluation
- **Description**: Compare an answer to the correct answer.  
- **JSON Output**:  
  ```json
  {
    "grade": "correct"
  }
  ```
  or `"partial"` / `"incorrect"`

### 33. ClassifyDifficultyOfQuestion
- **Description**: Rate difficulty as `"easy"`, `"medium"`, or `"hard"`.  
- **JSON Output**:
  ```json
  {
    "difficulty": "easy"
  }
  ```

### 34. IdentifyHumorTone
- **Description**: Check if text is intended to be humorous.  
- **JSON Output**:
  ```json
  {
    "is_humorous": true
  }
  ```
  or
  ```json
  {
    "is_humorous": false
  }
  ```

### 35. PhilippicOrConstructiveCriticism
- **Description**: Label critique as `"harsh"` or `"constructive"`.  
- **JSON Output**:  
  ```json
  {
    "critique_type": "constructive"
  }
  ```

### 36. MultiLabelTopicDetection
- **Description**: Return multiple possible topics from a set of potential labels.  
- **JSON Output**:  
  ```json
  {
    "topics": ["...", "..."]
  }
  ```

---

# 3) Extraction & Transformation (36 Tasks)

### 1. ExtractNamedEntities
- **Description**: Find named entities (people, places, events).  
- **JSON Output**:  
  ```json
  {
    "entities": ["...", "..."]
  }
  ```

### 2. ExtractKeyPhrases
- **Description**: Pull out the most relevant phrases.  
- **JSON Output**:  
  ```json
  {
    "key_phrases": ["...", "..."]
  }
  ```

### 3. ParseContactInfo
- **Description**: Extract phone, email, and address.  
- **JSON Output**:  
  ```json
  {
    "contact": {
      "phone": "...",
      "email": "...",
      "address": "..."
    }
  }
  ```

### 4. DateOfEvent
- **Description**: Find a mention of a date/time in text if it exists.  
- **JSON Output**:
  ```json
  {
    "date_time": "..."
  }
  ```
  or
  ```json
  {
    "date_time": null
  }
  ```

### 5. TransformIntoCSV
- **Description**: Convert a list of dictionaries → CSV-formatted string.  
- **JSON Output**:
  ```json
  {
    "csv": "col1,col2\nval1,val2\n..."
  }
  ```

### 6. ParseRSSFeedItem
- **Description**: Extract headline, link, date from an RSS snippet.  
- **JSON Output**:  
  ```json
  {
    "rss_item": {
      "headline": "...",
      "link": "...",
      "date": "..."
    }
  }
  ```

### 7. ExtractTablesFromHTML
- **Description**: Pull out table data as a list of tables (rows/cells).  
- **JSON Output**:  
  ```json
  {
    "tables": [
      [
        ["cell1","cell2"],
        ["cell3","cell4"]
      ]
    ]
  }
  ```

### 8. MarkdownToHTML
- **Description**: Convert Markdown text into HTML.  
- **JSON Output**:
  ```json
  {
    "html": "..."
  }
  ```

### 9. ExtractCodeSections
- **Description**: Find code blocks in text.  
- **JSON Output**:
  ```json
  {
    "code_blocks": ["...", "..."]
  }
  ```

### 10. TransformHrDocToJSON
- **Description**: Parse an HR doc, mapping each heading to a JSON key.  
- **JSON Output**:
  ```json
  {
    "hr_structure": {
      "Heading1": "...",
      "Heading2": "..."
    }
  }
  ```

### 11. NamedEntityPairExtraction
- **Description**: Return pairs of named entities found together.  
- **JSON Output**:
  ```json
  {
    "entity_pairs": [
      ["EntityA", "EntityB"],
      ["EntityC", "EntityD"]
    ]
  }
  ```

### 12. SummaryToBulletList
- **Description**: Split a summary into bullet points at sentence boundaries.  
- **JSON Output**:
  ```json
  {
    "bullet_points": ["...", "..."]
  }
  ```

### 13. ParseMLACitation
- **Description**: Extract authors, title, and publication info from MLA citation text.  
- **JSON Output**:
  ```json
  {
    "citation": {
      "authors": "...",
      "title": "...",
      "publisher": "...",
      ...
    }
  }
  ```

### 14. UnifyMeasurementUnits
- **Description**: Normalize measurements to a standard system (e.g., metric).  
- **JSON Output**:
  ```json
  {
    "normalized_text": "..."
  }
  ```

### 15. ExtractJobTitles
- **Description**: Identify job titles from a resume or CV text.  
- **JSON Output**:
  ```json
  {
    "job_titles": ["...", "..."]
  }
  ```

### 16. TransformAppReviewsToJSON
- **Description**: Parse lines of app reviews into structured JSON.  
- **JSON Output**:
  ```json
  [
    {
      "review": "...",
      "rating": "..."
    },
    ...
  ]
  ```

### 17. ParseRecipeInstructions
- **Description**: Extract ingredients and steps from a recipe.  
- **JSON Output**:
  ```json
  {
    "ingredients": ["...", "..."],
    "steps": ["...", "..."]
  }
  ```

### 18. CoordinatesExtractor
- **Description**: Find lat/long if present.  
- **JSON Output**:
  ```json
  {
    "coordinates": [12.34, -56.78]
  }
  ```
  or
  ```json
  {
    "coordinates": null
  }
  ```

### 19. StructureForumPosts
- **Description**: Convert forum text lines into structured fields (title, author, etc.).  
- **JSON Output**:
  ```json
  [
    {
      "title": "...",
      "author": "..."
    },
    ...
  ]
  ```

### 20. KeywordsWithFrequencies
- **Description**: Extract repeated keywords and their counts.  
- **JSON Output**:
  ```json
  {
    "keyword_counts": {
      "word1": 10,
      "word2": 3
    }
  }
  ```

### 21. ParseMusicPlaylistDescription
- **Description**: Extract track names/artists from playlist text.  
- **JSON Output**:
  ```json
  {
    "tracks": ["...", "..."]
  }
  ```

### 22. TransformChatTranscriptToJSON
- **Description**: Create a conversation structure with speaker, message, timestamp.  
- **JSON Output**:
  ```json
  [
    {
      "speaker": "...",
      "message": "...",
      "time": "..."
    },
    ...
  ]
  ```

### 23. ExtractCommonPhrasesAcrossDocs
- **Description**: Find recurring phrases across multiple documents.  
- **JSON Output**:
  ```json
  {
    "common_phrases": ["...", "..."]
  }
  ```

### 24. DocToOutline
- **Description**: Organize text by headings into an outline.  
- **JSON Output**:
  ```json
  {
    "outline": [
      "Heading1: details",
      "Heading2: details"
    ]
  }
  ```

### 25. RewriteToSchema
- **Description**: Parse text and map to each specified schema field.  
- **JSON Output**:
  ```json
  {
    "schema": {
      "field1": "...",
      "field2": "..."
    }
  }
  ```

### 26. ParseMathExpressions
- **Description**: Extract math formulas from text.  
- **JSON Output**:
  ```json
  {
    "expressions": ["...", "..."]
  }
  ```

### 27. StandardizeAddressFormat
- **Description**: Map a messy address block into a standardized format.  
- **JSON Output**:
  ```json
  {
    "address": {
      "street": "...",
      "city": "...",
      "zip": "..."
    }
  }
  ```

### 28. HighlightAndAnnotate
- **Description**: Find key sentences and annotate them with metadata.  
- **JSON Output**:
  ```json
  {
    "annotations": [
      {
        "text": "...",
        "note": "..."
      }
    ]
  }
  ```

### 29. PhoneNumbersFromLogs
- **Description**: Extract phone numbers from logs.  
- **JSON Output**:
  ```json
  {
    "phone_numbers": ["...", "..."]
  }
  ```

### 30. CombineAndDeduplicateRecords
- **Description**: Merge records describing the same entity into one unique set.  
- **JSON Output** (example):
  ```json
  [
    {
      "merged_record": {
        "id": 1,
        "name": "Example",
        ...
      }
    },
    ...
  ]
  ```

### 31. TransformXMLToJSON
- **Description**: Parse XML data into an equivalent JSON structure.  
- **JSON Output**:
  ```json
  {
    "json_data": {
      ...
    }
  }
  ```

### 32. ExtractHyperlinks
- **Description**: Find all hyperlink URLs in HTML.  
- **JSON Output**:
  ```json
  {
    "links": [
      "http://example.com",
      "https://another.com"
    ]
  }
  ```

### 33. MentionExtraction
- **Description**: Extract user mentions from text (e.g., `@username`).  
- **JSON Output**:
  ```json
  {
    "mentions": ["@User1", "@User2"]
  }
  ```

### 34. TransformParagraphsToList
- **Description**: Split text into paragraphs.  
- **JSON Output**:
  ```json
  {
    "paragraphs": ["paragraph1", "paragraph2", ...]
  }
  ```

### 35. ParseLogEntriesToFields
- **Description**: Turn log lines into structured fields (date, severity, message).  
- **JSON Output**:
  ```json
  [
    {
      "date": "...",
      "severity": "...",
      "message": "..."
    },
    ...
  ]
  ```

### 36. CodeDocstringExtractor
- **Description**: Find docstrings or comments in source code.  
- **JSON Output**:
  ```json
  {
    "docstrings": ["...", "..."]
  }
  ```

---

# 4) Question Answering & Context Retrieval (36 Tasks)

### 1. AnswerFactualQuestion
- **Description**: Directly answer a factual question from context.  
- **JSON Output**:
  ```json
  {
    "answer": "..."
  }
  ```

### 2. RetrieveDefinitionOfTerm
- **Description**: Look up a term’s definition in reference text.  
- **JSON Output**:
  ```json
  {
    "definition": "..."
  }
  ```

### 3. FindSpecificStatistic
- **Description**: Search for a numeric statistic in data text.  
- **JSON Output**:
  ```json
  {
    "statistic": "..."
  }
  ```

### 4. MultiPartQuestionAnswering
- **Description**: Answer multiple related questions from a single context.  
- **JSON Output**:
  ```json
  {
    "answers": ["...", "..."]
  }
  ```

### 5. HypothesizePossibleAnswers
- **Description**: Generate potential answers from multiple partial contexts.  
- **JSON Output**:
  ```json
  {
    "possible_answers": ["...", "..."]
  }
  ```

### 6. LawQuestionAnswer
- **Description**: Provide a direct legal Q&A using provided statutes.  
- **JSON Output**:
  ```json
  {
    "legal_answer": "..."
  }
  ```

### 7. AnswerWithQuotes
- **Description**: Give an answer plus a verbatim quote from context.  
- **JSON Output**:
  ```json
  {
    "answer": "...",
    "quote": "..."
  }
  ```

### 8. FindRelevantSection
- **Description**: Return the paragraph that best answers the question.  
- **JSON Output**:
  ```json
  {
    "relevant_section": "..."
  }
  ```

### 9. RankBestAnswers
- **Description**: Score candidate answers by relevance.  
- **JSON Output**:
  ```json
  {
    "ranked_answers": [
      ["Answer1", 0.9],
      ["Answer2", 0.7]
    ]
  }
  ```

### 10. TriviaQuestionSolver
- **Description**: Provide a concise answer to a trivia question.  
- **JSON Output**:
  ```json
  {
    "trivia_answer": "..."
  }
  ```

### 11. HighlightConfidenceAnswer
- **Description**: Return an answer and a confidence (0–1).  
- **JSON Output**:
  ```json
  {
    "answer": "...",
    "confidence": 0.85
  }
  ```

### 12. NestedQA
- **Description**: Split a large document, search each part, merge partial answers.  
- **JSON Output**:
  ```json
  {
    "answer": "..."
  }
  ```

### 13. FillInTheBlank
- **Description**: Complete a partially written prompt.  
- **JSON Output**:
  ```json
  {
    "completion": "..."
  }
  ```

### 14. HistoricalFactFinder
- **Description**: Answer a question about historical data.  
- **JSON Output**:
  ```json
  {
    "historical_answer": "..."
  }
  ```

### 15. ContextDrivenFAQ
- **Description**: Select or synthesize a FAQ entry from context.  
- **JSON Output**:
  ```json
  {
    "faq_answer": "..."
  }
  ```

### 16. StepByStepSolution
- **Description**: Provide a multi-step reasoning chain for a question.  
- **JSON Output**:
  ```json
  {
    "detailed_solution": "..."
  }
  ```

### 17. CodeDebugQA
- **Description**: Answer a question about code behavior or bugs.  
- **JSON Output**:
  ```json
  {
    "debug_answer": "..."
  }
  ```

### 18. LogicPuzzleSolver
- **Description**: Solve a short logic puzzle with reasoning.  
- **JSON Output**:
  ```json
  {
    "solution": "..."
  }
  ```

### 19. HighlightAllPossibleAnswers
- **Description**: Find every snippet that might answer a complex query.  
- **JSON Output**:
  ```json
  {
    "snippets": ["...", "..."]
  }
  ```

### 20. ConflictingAnswerHandler
- **Description**: Check multiple sources for contradictory answers.  
- **JSON Output**:
  ```json
  {
    "conflicts": {
      "source1": "answer1",
      "source2": "answer2"
    }
  }
  ```

### 21. FactualEvidenceCitation
- **Description**: Answer plus a text excerpt that supports the conclusion.  
- **JSON Output**:
  ```json
  {
    "answer": "...",
    "citation": "..."
  }
  ```

### 22. YesNoMaybeQuestion
- **Description**: Return `"yes"`, `"no"`, or `"maybe"` with a short justification.  
- **JSON Output**:
  ```json
  {
    "response": "yes",
    "justification": "..."
  }
  ```

### 23. MultiContextFusionAnswer
- **Description**: Fuse multiple contexts into a comprehensive answer.  
- **JSON Output**:
  ```json
  {
    "fusion_answer": "..."
  }
  ```

### 24. ShortAnswerCompletion
- **Description**: Supply a concise answer ignoring extended detail.  
- **JSON Output**:
  ```json
  {
    "short_answer": "..."
  }
  ```

### 25. EssayQuestionWriter
- **Description**: Generate an in-depth explanation from references.  
- **JSON Output**:
  ```json
  {
    "essay": "..."
  }
  ```

### 26. FillMissingInfo
- **Description**: Retrieve data for each missing field from context.  
- **JSON Output**:
  ```json
  {
    "field1": "...",
    "field2": "..."
  }
  ```

### 27. LocationBasedQuery
- **Description**: Answer location-based queries (addresses, directions, etc.).  
- **JSON Output**:
  ```json
  {
    "location_answer": "..."
  }
  ```

### 28. DirectQuotePassage
- **Description**: Return exact excerpt that best addresses the question.  
- **JSON Output**:
  ```json
  {
    "quoted_passage": "..."
  }
  ```

### 29. PolicyManualAnswer
- **Description**: Consult policy text to produce a relevant answer.  
- **JSON Output**:
  ```json
  {
    "policy_answer": "..."
  }
  ```

### 30. ShortDefinitionLookup
- **Description**: Find a short definition from a glossary.  
- **JSON Output**:
  ```json
  {
    "definition": "..."
  }
  ```

### 31. MultiDocReference
- **Description**: Attempt to answer from each doc if multiple docs exist.  
- **JSON Output**:
  ```json
  {
    "doc1": "...",
    "doc2": "..."
  }
  ```

### 32. CorrectCommonMisconceptions
- **Description**: Answer the question while clarifying typical misconceptions.  
- **JSON Output**:
  ```json
  {
    "explanation": "..."
  }
  ```

### 33. NumericAnswerExtractor
- **Description**: Parse a numeric answer from the data.  
- **JSON Output**:
  ```json
  {
    "value": 42.0
  }
  ```

### 34. InstructiveHowTo
- **Description**: Generate stepwise instructions for a “how-to” question.  
- **JSON Output**:
  ```json
  {
    "steps": ["Step1", "Step2"]
  }
  ```

### 35. FormulaDerivationQA
- **Description**: Derive or apply a math formula step by step.  
- **JSON Output**:
  ```json
  {
    "formula_solution": "..."
  }
  ```

### 36. UnifyMultipleAnswers
- **Description**: Merge partial answers from different sources into one.  
- **JSON Output**:
  ```json
  {
    "unified_answer": "..."
  }
  ```

---

# 5) Text Generation & Creative Writing (36 Tasks)

### 1. GeneratePoem
- **Description**: Compose a poem about a given theme.  
- **JSON Output**:
  ```json
  {
    "poem": "..."
  }
  ```

### 2. ShortStoryWriter
- **Description**: Write a short fictional narrative (with optional word limit).  
- **JSON Output**:
  ```json
  {
    "story": "..."
  }
  ```

### 3. GenerateBrandTagline
- **Description**: Produce a catchy brand tagline.  
- **JSON Output**:
  ```json
  {
    "tagline": "..."
  }
  ```

### 4. StylizedMotivationalQuote
- **Description**: Create a motivational quote in a specified style/tone.  
- **JSON Output**:
  ```json
  {
    "quote": "..."
  }
  ```

### 5. ComedicParodySketch
- **Description**: Write a short comedic parody of a scenario.  
- **JSON Output**:
  ```json
  {
    "parody": "..."
  }
  ```

### 6. RewriteInShakespeareanEnglish
- **Description**: Transform text into a Shakespearean style.  
- **JSON Output**:
  ```json
  {
    "shakespearean_text": "..."
  }
  ```

### 7. ChildrenStoryWithMoral
- **Description**: Generate a brief children’s story teaching a moral.  
- **JSON Output**:
  ```json
  {
    "story": "..."
  }
  ```

### 8. FuturisticSciFiScene
- **Description**: Create a scene set in a futuristic Sci-Fi world.  
- **JSON Output**:
  ```json
  {
    "scene": "..."
  }
  ```

### 9. RomanceMiniPlotSetup
- **Description**: Outline a romantic story with a key conflict.  
- **JSON Output**:
  ```json
  {
    "plot_outline": "..."
  }
  ```

### 10. ComedicDialogueSketch
- **Description**: Write a humorous dialogue between specified characters.  
- **JSON Output**:
  ```json
  {
    "dialogue": "..."
  }
  ```

### 11. FableCreationWithAnimals
- **Description**: Write a short fable with talking animals and a moral.  
- **JSON Output**:
  ```json
  {
    "fable": "..."
  }
  ```

### 12. ShortHaiku
- **Description**: Compose a 17-syllable haiku on a given topic.  
- **JSON Output**:
  ```json
  {
    "haiku": "..."
  }
  ```

### 13. SpeechForSpecialEvent
- **Description**: Draft a brief speech (wedding, graduation, etc.).  
- **JSON Output**:
  ```json
  {
    "speech": "..."
  }
  ```

### 14. RewriteAsEpicSaga
- **Description**: Expand a snippet into an epic heroic saga.  
- **JSON Output**:
  ```json
  {
    "epic_saga": "..."
  }
  ```

### 15. HistoricalAlternateRealityScene
- **Description**: Re-imagine a historical event differently.  
- **JSON Output**:
  ```json
  {
    "alternate_history": "..."
  }
  ```

### 16. HumorizeText
- **Description**: Make text comedic by adding humorous twists.  
- **JSON Output**:
  ```json
  {
    "comedic_version": "..."
  }
  ```

### 17. HorrorMicroStory
- **Description**: Create a very short horror story from a prompt.  
- **JSON Output**:
  ```json
  {
    "horror_story": "..."
  }
  ```

### 18. FairyTaleEndingGenerator
- **Description**: Generate a classic fairy tale style ending from a conflict scenario.  
- **JSON Output**:
  ```json
  {
    "fairy_tale_ending": "..."
  }
  ```

### 19. PuzzleRiddleGenerator
- **Description**: Create a riddle or puzzle around a given topic.  
- **JSON Output**:
  ```json
  {
    "riddle": "..."
  }
  ```

### 20. RewriteAsDystopianIntro
- **Description**: Turn text into a dystopian opening paragraph.  
- **JSON Output**:
  ```json
  {
    "dystopian_intro": "..."
  }
  ```

### 21. ComedicInsultGenerator
- **Description**: Generate playful, mild comedic insults.  
- **JSON Output**:
  ```json
  {
    "insult": "..."
  }
  ```

### 22. PirateStyleTranslation
- **Description**: Rewrite text with pirate expressions (e.g. “Ahoy”).  
- **JSON Output**:
  ```json
  {
    "pirate_text": "..."
  }
  ```

### 23. RewriteWithSarcasticTone
- **Description**: Convert neutral text into a sarcastic version.  
- **JSON Output**:
  ```json
  {
    "sarcastic_text": "..."
  }
  ```

### 24. ImagineAlienDialogue
- **Description**: Create a dialogue between alien beings on a new planet.  
- **JSON Output**:
  ```json
  {
    "alien_dialogue": "..."
  }
  ```

### 25. ComedicProductReview
- **Description**: Write a humorous, ad-style review for a product.  
- **JSON Output**:
  ```json
  {
    "comedic_review": "..."
  }
  ```

### 26. FreestyleRapLyrics
- **Description**: Generate rap lyrics about a topic.  
- **JSON Output**:
  ```json
  {
    "rap_lyrics": "..."
  }
  ```

### 27. ComedicObituaryPrompt
- **Description**: Write a satirical, lighthearted obituary.  
- **JSON Output**:
  ```json
  {
    "obituary": "..."
  }
  ```

### 28. CondescendingPersuasion
- **Description**: Rewrite text as if persuading someone from a superior vantage point, humorous.  
- **JSON Output**:
  ```json
  {
    "condescending_version": "..."
  }
  ```

### 29. RewriteAsIfSpokenByRobot
- **Description**: Add mechanical, robotic speech patterns.  
- **JSON Output**:
  ```json
  {
    "robot_text": "..."
  }
  ```

### 30. KidsJokeGenerator
- **Description**: Create a family-friendly joke about a given topic.  
- **JSON Output**:
  ```json
  {
    "kids_joke": "..."
  }
  ```

### 31. ActionSceneDescription
- **Description**: Generate an intense, cinematic action scene.  
- **JSON Output**:
  ```json
  {
    "action_scene": "..."
  }
  ```

### 32. MonologueForVillain
- **Description**: Write a dramatic villain monologue.  
- **JSON Output**:
  ```json
  {
    "villain_monologue": "..."
  }
  ```

### 33. ComedicAutoReplyEmail
- **Description**: Generate a funny out-of-office auto-reply.  
- **JSON Output**:
  ```json
  {
    "auto_reply": "..."
  }
  ```

### 34. LivingObjectAnthropomorphicStory
- **Description**: Narrate a story from an inanimate object’s perspective.  
- **JSON Output**:
  ```json
  {
    "object_story": "..."
  }
  ```

### 35. RewriteIntoSongChorus
- **Description**: Transform text into a chorus in a specified music genre.  
- **JSON Output**:
  ```json
  {
    "chorus": "..."
  }
  ```

### 36. CrossOverFanFiction
- **Description**: Merge characters from different universes into a short fanfic piece.  
- **JSON Output**:
  ```json
  {
    "fan_fiction": "..."
  }
  ```

---

# 6) Analytics & Data Insights (36 Tasks)

### 1. BasicSentimentStats
- **Description**: Count how many texts are positive, negative, or neutral (percentages).  
- **JSON Output**:
  ```json
  {
    "positive": 40.0,
    "negative": 35.0,
    "neutral": 25.0
  }
  ```

### 2. TopNWords
- **Description**: Identify the N most frequent words in text.  
- **JSON Output**:
  ```json
  {
    "top_words": ["word1", "word2", ...]
  }
  ```

### 3. AverageSentenceLength
- **Description**: Compute mean sentence length.  
- **JSON Output**:
  ```json
  {
    "avg_sentence_length": 12.3
  }
  ```

### 4. NGramFrequency
- **Description**: Find frequencies of n-grams in text.  
- **JSON Output**:
  ```json
  {
    "ngrams": {
      "hello world": 5,
      "test phrase": 2
    }
  }
  ```

### 5. ReadingLevelEstimation
- **Description**: Estimate reading level (e.g. `"Grade 9"`).  
- **JSON Output**:
  ```json
  {
    "reading_level": "Grade 9"
  }
  ```

### 6. StanceAnalysis
- **Description**: Count how many texts are pro, against, or neutral on an issue.  
- **JSON Output**:
  ```json
  {
    "pro": 10,
    "against": 5,
    "neutral": 3
  }
  ```

### 7. TimelineOfEvents
- **Description**: Identify chronological references and order them.  
- **JSON Output**:
  ```json
  {
    "events": [
      {"date": "...", "description": "..."},
      ...
    ]
  }
  ```

### 8. CorrelationOfKeywords
- **Description**: Show how often given keywords appear together.  
- **JSON Output**:
  ```json
  {
    "co_occurrences": {
      ["keyword1","keyword2"]: 10,
      ["keyword3","keyword4"]: 3
    }
  }
  ```

### 9. AverageParagraphComplexity
- **Description**: Compute an average complexity score per paragraph.  
- **JSON Output**:
  ```json
  {
    "complexity_score": 0.75
  }
  ```

### 10. MultiDocumentTopicModeling
- **Description**: Discover main topics across multiple docs.  
- **JSON Output**:
  ```json
  {
    "topics": {
      "topicA": [0, 2],
      "topicB": [1]
    }
  }
  ```

### 11. TfIdfRanking
- **Description**: Calculate TF-IDF for given terms.  
- **JSON Output**:
  ```json
  {
    "tfidf_scores": {
      "term1": 0.12,
      "term2": 0.05
    }
  }
  ```

### 12. CompareReviewScores
- **Description**: Compute average rating by category from text/score pairs.  
- **JSON Output**:
  ```json
  {
    "averages": {
      "plot": 8.1,
      "acting": 7.4
    }
  }
  ```

### 13. IdentifyOutliersInTextLengths
- **Description**: Flag abnormally long/short docs among many.  
- **JSON Output**:
  ```json
  {
    "outliers": [0, 5, 22]
  }
  ```

### 14. PositivityVsNegativityTrend
- **Description**: Calculate positivity ratio per item over time.  
- **JSON Output**:
  ```json
  {
    "trend": [
      {"index": 0, "ratio": 0.8},
      ...
    ]
  }
  ```

### 15. ComputeSyntacticDiversity
- **Description**: Estimate how varied the syntax is.  
- **JSON Output**:
  ```json
  {
    "syntactic_diversity": 0.54
  }
  ```

### 16. MeasureRepetitivePhrases
- **Description**: Count repeated phrases throughout text.  
- **JSON Output**:
  ```json
  {
    "repetitions": {
      "phrase1": 4,
      "phrase2": 2
    }
  }
  ```

### 17. DetectReadabilityDropOff
- **Description**: Flag paragraphs that are too dense or complex.  
- **JSON Output**:
  ```json
  {
    "difficult_paragraphs": [1, 3]
  }
  ```

### 18. ProgressiveToneAnalysis
- **Description**: Track how tone changes from one text to the next (e.g., `"neutral"` → `"positive"`).  
- **JSON Output**:
  ```json
  {
    "tone_progression": ["neutral", "positive", "negative"]
  }
  ```

### 19. GatherEntityFrequencyAcrossDocs
- **Description**: Count mentions of each known entity across docs.  
- **JSON Output**:
  ```json
  {
    "entity_counts": {
      "Entity1": 15,
      "Entity2": 3
    }
  }
  ```

### 20. CompareHeadersAcrossDocuments
- **Description**: Check which docs contain which headings.  
- **JSON Output**:
  ```json
  {
    "headingA": [true, false, true],
    "headingB": [false, false, true]
  }
  ```

### 21. TrackPolarizingKeywords
- **Description**: Count occurrences of loaded terms in a corpus.  
- **JSON Output**:
  ```json
  {
    "keyword_counts": {
      "keyword1": 10,
      "keyword2": 5
    }
  }
  ```

### 22. SummarizeFeedbackTrends
- **Description**: Analyze overall sentiment/themes in user feedback.  
- **JSON Output**:
  ```json
  {
    "summary": "..."
  }
  ```

### 23. StoryArcDetection
- **Description**: Identify exposition, climax, resolution segments in a story.  
- **JSON Output**:
  ```json
  {
    "story_arc": [
      "exposition at paragraph 1",
      "climax at paragraph 3"
    ]
  }
  ```

### 24. AggregatedEmotionHistogram
- **Description**: Generate histogram of emotional categories.  
- **JSON Output**:
  ```json
  {
    "emotion_histogram": {
      "joy": 10,
      "anger": 5,
      "sadness": 8
    }
  }
  ```

### 25. ConflictingOpinionExtractor
- **Description**: Find pairs of contradictory statements.  
- **JSON Output**:
  ```json
  {
    "conflicts": [
      ["stmt1", "stmt2"],
      ["stmtA", "stmtB"]
    ]
  }
  ```

### 26. AdvancedKeywordContextMap
- **Description**: Store context windows around keywords.  
- **JSON Output**:
  ```json
  {
    "keyword_context": {
      "keyword1": ["context snippet1", "snippet2"],
      "keyword2": ["context snippet3"]
    }
  }
  ```

### 27. PerformanceReviewInsight
- **Description**: Identify recurring compliments/criticisms from reviews.  
- **JSON Output**:
  ```json
  {
    "compliments": ["...", "..."],
    "criticisms": ["...", "..."]
  }
  ```

### 28. BrandPerceptionAnalysis
- **Description**: Calculate brand sentiment or loyalty from text.  
- **JSON Output**:
  ```json
  {
    "brand_sentiment": {
      "sentiment_score": 0.8,
      "notes": "..."
    }
  }
  ```

### 29. CompetitorMentionsFrequency
- **Description**: Count references to each competitor.  
- **JSON Output**:
  ```json
  {
    "competitor_counts": {
      "CompetitorA": 3,
      "CompetitorB": 1
    }
  }
  ```

### 30. StoryCohesionScore
- **Description**: Score how logically coherent a narrative is.  
- **JSON Output**:
  ```json
  {
    "cohesion_score": 0.9
  }
  ```

### 31. AdvancedSpellingAndGrammarStats
- **Description**: Count grammar/spelling errors, provide an overall score.  
- **JSON Output**:
  ```json
  {
    "error_counts": {
      "spelling": 3,
      "grammar": 2
    },
    "score": 0.85
  }
  ```

### 32. FragmentationAnalysis
- **Description**: Measure how often the text changes topic/viewpoint.  
- **JSON Output**:
  ```json
  {
    "fragmentation_score": 0.4
  }
  ```

### 33. RepeatedQuestionDetection
- **Description**: List any repeated questions in a text.  
- **JSON Output**:
  ```json
  {
    "repeated_questions": ["...", "..."]
  }
  ```

### 34. MultiAuthorTextAnalysis
- **Description**: Analyze style features to see how each segment might differ by author.  
- **JSON Output**:
  ```json
  {
    "segment_analysis": {
      "1": {"vocab_richness": 0.7, ...},
      "2": {...}
    }
  }
  ```

### 35. MeasureLinguisticStyleShift
- **Description**: Score how different two texts are in style/vocabulary.  
- **JSON Output**:
  ```json
  {
    "style_diff_score": 0.75
  }
  ```

### 36. ConversationTurnAnalysis
- **Description**: Count how many times each participant speaks, plus average turn length.  
- **JSON Output**:
  ```json
  {
    "turn_data": {
      "UserA": {
        "turns": 5,
        "avg_length": 15
      },
      "UserB": {
        "turns": 3,
        "avg_length": 10
      }
    }
  }
  ```

---

# 7) User Interaction & Communication Tasks (36 Tasks)

### 1. GeneratePersonalizedEmailGreeting
- **Description**: Create a warm, personal greeting for an email.  
- **JSON Output**:
  ```json
  {
    "greeting": "..."
  }
  ```

### 2. ComposeCustomerSupportEmail
- **Description**: Draft a polite response outlining steps to resolve a user’s issue.  
- **JSON Output**:
  ```json
  {
    "support_email": "..."
  }
  ```

### 3. RewriteInBriefTextMessageForm
- **Description**: Condense a paragraph into a short text message.  
- **JSON Output**:
  ```json
  {
    "text_message": "..."
  }
  ```

### 4. GenerateFormalApologyEmail
- **Description**: Create a formal apology letter.  
- **JSON Output**:
  ```json
  {
    "apology_email": "..."
  }
  ```

### 5. AppointmentReminderMessage
- **Description**: A short, friendly reminder of an upcoming appointment.  
- **JSON Output**:
  ```json
  {
    "reminder_message": "..."
  }
  ```

### 6. ReRankHelpArticles
- **Description**: Sort help articles by relevance to a user’s query.  
- **JSON Output**:
  ```json
  {
    "re_ranked": ["article1", "article2", "..."]
  }
  ```

### 7. PrioritizeCustomerQueries
- **Description**: Order user queries from highest to lowest priority.  
- **JSON Output**:
  ```json
  {
    "sorted_queries": ["...", "..."]
  }
  ```

### 8. MeetingAgendaGenerator
- **Description**: Create a structured meeting agenda with relevant points.  
- **JSON Output**:
  ```json
  {
    "agenda": "..."
  }
  ```

### 9. FormalAnnouncementDraft
- **Description**: Produce a polished formal announcement from details.  
- **JSON Output**:
  ```json
  {
    "announcement": "..."
  }
  ```

### 10. JobOfferLetter
- **Description**: Write a formal job offer letter with position, salary, etc.  
- **JSON Output**:
  ```json
  {
    "offer_letter": "..."
  }
  ```

### 11. ReorderSupportTickets
- **Description**: Sort tickets based on policy for severity.  
- **JSON Output**:
  ```json
  {
    "sorted_tickets": ["ticket1", "ticket2"]
  }
  ```

### 12. UserFeedbackAutoReply
- **Description**: Generate a quick “thank you” response for user feedback.  
- **JSON Output**:
  ```json
  {
    "auto_reply": "..."
  }
  ```

### 13. MarketingEmailForNewFeature
- **Description**: Write a promotional email about a new product feature.  
- **JSON Output**:
  ```json
  {
    "marketing_email": "..."
  }
  ```

### 14. InvoiceReminderEmail
- **Description**: Draft a friendly invoice payment reminder.  
- **JSON Output**:
  ```json
  {
    "reminder_email": "..."
  }
  ```

### 15. InternalUpdateMessage
- **Description**: Compose a short Slack/Teams update for a specific team.  
- **JSON Output**:
  ```json
  {
    "update_message": "..."
  }
  ```

### 16. UserEscalationHandler
- **Description**: Draft a calm, solution-oriented response to a user escalation.  
- **JSON Output**:
  ```json
  {
    "escalation_response": "..."
  }
  ```

### 17. ResumeCoverLetterTemplate
- **Description**: Generate a cover letter “skeleton” for a job application.  
- **JSON Output**:
  ```json
  {
    "cover_letter": "..."
  }
  ```

### 18. ProductReturnApprovalEmail
- **Description**: Write a formal notice approving a product return.  
- **JSON Output**:
  ```json
  {
    "return_approval": "..."
  }
  ```

### 19. WorkshopInvitation
- **Description**: Construct an invitation for a workshop (date, location, RSVP).  
- **JSON Output**:
  ```json
  {
    "invitation": "..."
  }
  ```

### 20. UserOnboardingInstructions
- **Description**: Generate step-by-step welcome instructions for a new user.  
- **JSON Output**:
  ```json
  {
    "onboarding_guide": "..."
  }
  ```

### 21. PoliteMeetingRescheduleEmail
- **Description**: Request to reschedule a meeting politely.  
- **JSON Output**:
  ```json
  {
    "reschedule_email": "..."
  }
  ```

### 22. ReRankContactMethods
- **Description**: Order ways to contact a user by preference/effectiveness.  
- **JSON Output**:
  ```json
  {
    "ranked_methods": ["method1", "method2"]
  }
  ```

### 23. DailyBulletinAnnouncement
- **Description**: Summarize daily internal news items.  
- **JSON Output**:
  ```json
  {
    "bulletin": "..."
  }
  ```

### 24. PersonalizedFollowupEmail
- **Description**: Follow-up email referencing a previous conversation/event.  
- **JSON Output**:
  ```json
  {
    "followup_email": "..."
  }
  ```

### 25. ReRankAppNotifications
- **Description**: Sort notifications by importance or urgency.  
- **JSON Output**:
  ```json
  {
    "notifications": ["notif1", "notif2"]
  }
  ```

### 26. VolunteerRecruitmentMessage
- **Description**: Draft a call-to-action asking for event volunteers.  
- **JSON Output**:
  ```json
  {
    "recruitment_email": "..."
  }
  ```

### 27. WriteCongratulatoryNote
- **Description**: Compose a short note congratulating someone on a milestone.  
- **JSON Output**:
  ```json
  {
    "congrats_note": "..."
  }
  ```

### 28. ReRankForumQuestions
- **Description**: Order forum questions by relevance to user interests.  
- **JSON Output**:
  ```json
  {
    "sorted_questions": ["q1", "q2"]
  }
  ```

### 29. ScheduleUpdateNotification
- **Description**: Summarize schedule changes and notify recipients.  
- **JSON Output**:
  ```json
  {
    "update_notification": "..."
  }
  ```

### 30. ReRankProductSearchResults
- **Description**: Sort product search results by query relevance.  
- **JSON Output**:
  ```json
  {
    "sorted_results": ["product1", "product2"]
  }
  ```

### 31. HolidayGreetingMessage
- **Description**: Create a festive greeting for a specified holiday.  
- **JSON Output**:
  ```json
  {
    "greeting": "..."
  }
  ```

### 32. ProjectKickoffEmail
- **Description**: Announce a new project with immediate action items.  
- **JSON Output**:
  ```json
  {
    "kickoff_email": "..."
  }
  ```

### 33. AutoThankYouForFeedback
- **Description**: Generate an automated thank-you for feedback.  
- **JSON Output**:
  ```json
  {
    "thank_you": "..."
  }
  ```

### 34. CodeOfConductReminder
- **Description**: Remind a group about code of conduct/policy guidelines.  
- **JSON Output**:
  ```json
  {
    "reminder": "..."
  }
  ```

### 35. SponsorRenewalRequestEmail
- **Description**: Invite a sponsor to renew their support for an event.  
- **JSON Output**:
  ```json
  {
    "renewal_request": "..."
  }
  ```

### 36. NextStepsFollowupAfterMeeting
- **Description**: Summarize a meeting’s next steps with owners.  
- **JSON Output**:
  ```json
  {
    "followup": "..."
  }
  ```

---

## Generic Usage Example

Below is a generic usage example. You can substitute any of the above task classes in place of `<TaskName>`:

```python
import os
import json
from flashlearn.skills import GeneralSkill
from flashlearn.skills.toolkit import <TaskName>

def main():
    # Optional: Provide your OpenAI key (or other LLM provider)
    # os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

    # Example data: A list of text documents
    data = [
        {"text": "This is a sample document. It needs rewriting or summarizing."},
        {"text": "Another text block to process."}
    ]

    # Load the skill definition
    skill = GeneralSkill.load_skill(<TaskName>)

    # Transform your data into tasks
    tasks = skill.create_tasks(data)

    # Run tasks (parallels by default)
    results = skill.run_tasks_in_parallel(tasks)

    # Output is guaranteed JSON
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
```

**All tasks follow a similar pattern**:  
1. Load the skill’s “definition” from the toolkit.  
2. Create tasks by passing your input data (e.g., text).  
3. Run tasks to get valid JSON outputs.

---

## Conclusion

This reference lists every built-in task in the FlashLearn toolkit. You can pick from any to classify text, generate new copy, summarize documents, extract structured info, or handle user communication—always with guaranteed JSON responses.

1. Zero custom training required: just pick a task.  
2. Combine tasks in multi-step workflows to power robust NLP pipelines.  
3. Outputs are strictly JSON for reliability and easy chaining.

**Happy building with FlashLearn!**  