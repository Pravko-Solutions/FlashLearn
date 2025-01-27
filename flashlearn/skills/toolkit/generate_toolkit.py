import os

from flashlearn.skills.learn_skill import LearnSkill
import plotly.express as px

def main():
    # Step 1: Provide your OpenAI
    # os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'
    os.environ["OPENAI_API_KEY"] = (
        "sk-proj-Ts1lBu6Jc0YHCRTYVb00sXRfc_nUgGI7qcrKfCyDxvTn06qcpehsVL_6n2LhuP5qC7"
        "XEh1W4AET3BlbkFJm8kpzJWs9PXQ4zUTyHawJYs1vdMsH1Axa06_e__JcaGl7PhzRe8Ab2Yg5fTm"
        "GL8eK39jFX2b4A"
    )
    tasks = [
        # 1) SUMMARIZATION & REWRITING (36 Tasks)
        {
            "name": "SummarizeText",
            "task": "Given a long document, produce a short summary. Return it in JSON as {\"summary\": \"...\"} with 2-5 sentences highlighting main points."
        },
        {
            "name": "BulletPointSummary",
            "task": "Convert the given document into concise bullet points. Return a JSON object {\"bullet_points\": [\"point1\", \"point2\"]} capturing the main ideas."
        },
        {
            "name": "HighlightKeyPoints",
            "task": "Extract the key ideas from the provided text and list them. Format your output as a JSON object {\"key_points\": [\"...\", \"...\"]}."
        },
        {
            "name": "ParagraphReduction",
            "task": "Condense the paragraph by a given reduction factor. Return a single string inside JSON: {\"reduced_paragraph\": \"...\"}."
        },
        {
            "name": "RewriteInFormalTone",
            "task": "Rewrite the text in a more formal, academic style. Output a JSON object {\"formal_text\": \"...\"}."
        },
        {
            "name": "RewriteForChildren",
            "task": "Adapt text for a younger reading audience. Return a simplified version inside JSON: {\"child_friendly\": \"...\"}."
        },
        {
            "name": "SummaryWithQuotes",
            "task": "Summarize the text while keeping a few original quotes verbatim. Return JSON with {\"summary\": \"...\"}."
        },
        {
            "name": "MultiLanguageSummary",
            "task": "Provide short summaries in multiple languages. Return a JSON object where keys are language codes and values are summaries, e.g. {\"en\": \"...\", \"es\": \"...\"}."
        },
        {
            "name": "HeadlineGenerator",
            "task": "Given the text, produce a single catchy headline. Return JSON: {\"headline\": \"...\"}."
        },
        {
            "name": "BulletedSynopsis",
            "task": "Summarize text into bullet points using a custom bullet prefix. Return {\"synopsis_bullets\": [\"...\", \"...\"]}."
        },
        {
            "name": "RewritePassiveToActive",
            "task": "Rewrite sentences so they use active voice. Return {\"active_voice_text\": \"...\"}."
        },
        {
            "name": "MultiParagraphSummary",
            "task": "Summarize the original document into a specified number of paragraphs. Return {\"paragraphs\": [\"...\"]}."
        },
        {
            "name": "ThematicSummary",
            "task": "Generate short summaries of each theme from a list of provided themes. Return a JSON map, e.g. {\"theme1\": \"...\", \"theme2\": \"...\"}."
        },
        {
            "name": "ExecutiveBrief",
            "task": "Condense the text into a concise executive summary with key takeaways. Return {\"executive_summary\": \"...\"}."
        },
        {
            "name": "RewriteInQnAFormat",
            "task": "Transform the content into a list of Q&A pairs. Return {\"qa_pairs\": [[\"Question\", \"Answer\"], [\"Q2\", \"A2\"]]}."
        },
        {
            "name": "RewriteAsPressRelease",
            "task": "Produce a formal press release version of the text. Return {\"press_release\": \"...\"}."
        },
        {
            "name": "HighlightActionItems",
            "task": "Extract action items or tasks from a meeting note or plan. Return {\"action_items\": [\"...\"]}."
        },
        {
            "name": "SimplifyForNonExperts",
            "task": "Rewrite technical content in simple, plain language. Return {\"simple_explanation\": \"...\"}."
        },
        {
            "name": "AcademicAbstract",
            "task": "Generate an academic-style abstract summarizing the document. Return {\"abstract\": \"...\"}."
        },
        {
            "name": "HighlightAndExpand",
            "task": "Find crucial lines in the text and provide expansions or definitions for each. Return {\"highlights\": [{\"text\": \"...\", \"expansion\": \"...\"}]}."
        },
        {
            "name": "RewriteSentencesAsBulletPoints",
            "task": "Convert each sentence of the text into a bullet point. Return {\"bullets\": [\"...\"]}."
        },
        {
            "name": "SummarizeDialogue",
            "task": "Summarize a conversation or meeting transcript into its major points. Return {\"dialogue_summary\": \"...\"}."
        },
        {
            "name": "StoryToFactSheet",
            "task": "Extract factual data from a narrative and place it into labeled fields in JSON, e.g. {\"facts\": {\"location\": \"...\", \"characters\": \"...\"}}."
        },
        {
            "name": "ExtractImportantFigures",
            "task": "Extract numbers, stats, or key facts from the text. Return {\"figures\": [\"...\"]}."
        },
        {
            "name": "CreateShortDescription",
            "task": "Produce a concise promotional or meta description from the text. Return {\"short_description\": \"...\"}."
        },
        {
            "name": "RewriteLegaleseInPlainLanguage",
            "task": "Convert ‘legalese’ text into clear, plain-language statements. Return {\"plain_language\": \"...\"}."
        },
        {
            "name": "CreateSloganVersion",
            "task": "Generate a one-liner slogan from the text. Return {\"slogan\": \"...\"}."
        },
        {
            "name": "RewriteInThirdPerson",
            "task": "Convert first-person references in the text to third-person. Return {\"third_person_text\": \"...\"}."
        },
        {
            "name": "RewordForPositiveTone",
            "task": "Adjust the phrasing of the text to have a more positive or uplifting tone. Return {\"positive_version\": \"...\"}."
        },
        {
            "name": "MultiSectionSummary",
            "task": "Break the document into sections and summarize each with given titles. Return {\"sections\": {\"title1\": \"summary\", \"title2\": \"summary\"}}."
        },
        {
            "name": "RewriteWithAdditionalContext",
            "task": "Insert extra contextual information into the original text seamlessly. Return {\"augmented_text\": \"...\"}."
        },
        {
            "name": "ShortParagraphSynopsis",
            "task": "Create a single-sentence summary of a larger paragraph. Return {\"synopsis\": \"...\"}."
        },
        {
            "name": "RewriteIntoBlogIntroduction",
            "task": "Turn a piece of text into a blog-style introduction paragraph. Return {\"blog_intro\": \"...\"}."
        },
        {
            "name": "HighlightSafetyWarnings",
            "task": "Extract important disclaimers or safety warnings from the text. Return {\"warnings\": [\"...\"]}."
        },
        {
            "name": "RewriteAsStory",
            "task": "Transform the text into a short narrative featuring specific characters. Return {\"story\": \"...\"}."
        },
        {
            "name": "GenerateTableOfContents",
            "task": "Create a conceptual table of contents for the text based on topics. Return {\"table_of_contents\": [\"...\"]}."
        },

        # 2) CLASSIFICATION & LABELING (36 Tasks)
        {
            "name": "ClassifyReviewSentiment",
            "task": "Label each review as 'positive', 'negative', or 'neutral'. Return JSON: {\"sentiment\": \"...\"}."
        },
        {
            "name": "DetectSpamMessage",
            "task": "Classify whether a message is spam (true/false). Return {\"is_spam\": true} or {\"is_spam\": false}."
        },
        {
            "name": "LanguageOfText",
            "task": "Identify the language of the input text. Return {\"language\": \"...\"}."
        },
        {
            "name": "CategorizeNewsArticle",
            "task": "Map a news article to a broad category (e.g., 'sports', 'politics', etc.). Return {\"category\": \"...\"}."
        },
        {
            "name": "LabelTechSupportTickets",
            "task": "Classify support tickets by urgency (e.g., 'low', 'medium', 'high'). Return {\"urgency\": \"...\"}."
        },
        {
            "name": "TopicModelingSnippet",
            "task": "Identify possible topics or themes in a snippet. Return {\"topics\": [\"...\"]}."
        },
        {
            "name": "EmotionalToneDetection",
            "task": "Provide intensity scores for emotions like joy, anger, sadness. Return JSON with each emotion and a float score, e.g. {\"joy\": 0.8, \"anger\": 0.2}."
        },
        {
            "name": "DomainSpecificClassification",
            "task": "Use a given domain context (e.g., 'medical') to refine classification of the text. Return {\"classification\": \"...\"}."
        },
        {
            "name": "ClassifyCodeSnippetLanguage",
            "task": "Identify the programming language of a code snippet. Return {\"language\": \"...\"}."
        },
        {
            "name": "BrandMentionDetector",
            "task": "Detect brand references from a brand list. Return a map brand->found, e.g. {\"BrandA\": true, \"BrandB\": false}."
        },
        {
            "name": "IdentifyControversialContent",
            "task": "Label if content is potentially sensitive or controversial. Return {\"controversial\": true/false}."
        },
        {
            "name": "CategoryPredictionFromKeywords",
            "task": "Match text to a predefined set of categories using keywords. Return {\"category\": \"...\"}."
        },
        {
            "name": "ClassifyQualityOfWriting",
            "task": "Label writing as 'excellent', 'good', or 'needs work'. Return {\"quality\": \"...\"}."
        },
        {
            "name": "SeriousnessOfComplaint",
            "task": "Rank complaint severity from 'minor' to 'major'. Return {\"severity\": \"...\"}."
        },
        {
            "name": "MusicGenreClassification",
            "task": "Predict the music genre from a descriptive text. Return {\"music_genre\": \"...\"}."
        },
        {
            "name": "ImageCaptionsToSceneCategory",
            "task": "Classify an image caption (e.g., 'indoors', 'outdoors', 'crowd'). Return {\"scene_category\": \"...\"}."
        },
        {
            "name": "ClassifyCommentSection",
            "task": "Classify multiple user comments as 'toxic', 'spam', 'relevant', etc. Return a list of labels for each comment: {\"comment_labels\": [\"toxic\", \"spam\"]}."
        },
        {
            "name": "ClassifyLegalDocumentType",
            "task": "Identify the type of a legal document (e.g., 'contract', 'will', 'complaint'). Return {\"legal_type\": \"...\"}."
        },
        {
            "name": "LocationCategorySnippet",
            "task": "Classify a snippet about a place (e.g., 'tourist spot', 'historical site'). Return {\"location_type\": \"...\"}."
        },
        {
            "name": "TimelineEventClassifier",
            "task": "Tag an event description into a timeline category (e.g., 'political', 'social'). Return {\"event_category\": \"...\"}."
        },
        {
            "name": "SkillLevelAssessment",
            "task": "Classify someone's skill level in a domain (e.g., 'beginner', 'intermediate', 'expert'). Return {\"skill_level\": \"...\"}."
        },
        {
            "name": "ClassifyGenreOfBlurb",
            "task": "Tag a short text as 'romance', 'mystery', 'sci-fi', or other literary genre. Return {\"genre\": \"...\"}."
        },
        {
            "name": "JobPostClassification",
            "task": "Label a job posting by field (IT, HR, marketing, etc.). Return {\"field\": \"...\"}."
        },
        {
            "name": "IdentifyHealthyVsUnhealthyRecipe",
            "task": "Decide if a recipe is generally healthy or not. Return {\"healthiness\": \"healthy\" or \"unhealthy\"}."
        },
        {
            "name": "LabelSarcasmInTweet",
            "task": "Detect if a tweet is sarcastic. Return {\"sarcastic\": true/false}."
        },
        {
            "name": "SkillBasedRoutingHandler",
            "task": "Classify a support case to route it to the correct specialized agent. Return {\"route_to\": \"...\"}."
        },
        {
            "name": "ClothingItemClassifier",
            "task": "Tag an item description as 'shirt', 'pants', 'shoes', etc. Return {\"clothing_type\": \"...\"}."
        },
        {
            "name": "ProfanityFilter",
            "task": "Flag if the text contains strong profanity. Return {\"contains_profanity\": true/false}."
        },
        {
            "name": "ClassifyMarketingHeadline",
            "task": "Label a marketing headline's style (e.g., 'discount-based', 'emotional', 'urgency'). Return {\"headline_style\": \"...\"}."
        },
        {
            "name": "ProductReviewSatisfactionLevel",
            "task": "Classify how satisfied the customer is (low, medium, high). Return {\"satisfaction\": \"...\"}."
        },
        {
            "name": "UserMoodAnalysis",
            "task": "Label a user's mood: 'excited', 'frustrated', etc. Return {\"mood\": \"...\"}."
        },
        {
            "name": "ShortAnswerGradedEvaluation",
            "task": "Compare an answer to the correct answer. Return {\"grade\": \"correct\", \"partial\", or \"incorrect\"}."
        },
        {
            "name": "ClassifyDifficultyOfQuestion",
            "task": "Rate question difficulty as 'easy', 'medium', or 'hard'. Return {\"difficulty\": \"...\"}."
        },
        {
            "name": "IdentifyHumorTone",
            "task": "Check if text is intended to be humorous. Return {\"is_humorous\": true/false}."
        },
        {
            "name": "PhilippicOrConstructiveCriticism",
            "task": "Label critique as 'harsh' or 'constructive'. Return {\"critique_type\": \"...\"}."
        },
        {
            "name": "MultiLabelTopicDetection",
            "task": "Return multiple possible topics from a set of potential labels. Return {\"topics\": [\"...\"]}."
        },

        # 3) EXTRACTION & TRANSFORMATION (36 Tasks)
        {
            "name": "ExtractNamedEntities",
            "task": "Find named entities (people, places, events) in text. Return {\"entities\": [\"...\"]}."
        },
        {
            "name": "ExtractKeyPhrases",
            "task": "Pull out the most relevant phrases. Return {\"key_phrases\": [\"...\"]}."
        },
        {
            "name": "ParseContactInfo",
            "task": "Extract phone, email, address from textual data. Return {\"contact\": {\"phone\": \"...\", \"email\": \"...\", \"address\": \"...\"}}."
        },
        {
            "name": "DateOfEvent",
            "task": "Find a mention of a date or time in text. Return {\"date_time\": \"...\"} or {\"date_time\": null} if none found."
        },
        {
            "name": "TransformIntoCSV",
            "task": "Given a list of dictionaries, convert to a CSV-formatted string. Return {\"csv\": \"...\"}."
        },
        {
            "name": "ParseRSSFeedItem",
            "task": "Extract headline, link, date from an RSS feed snippet. Return {\"rss_item\": {\"headline\": \"...\", \"link\": \"...\", \"date\": \"...\"}}."
        },
        {
            "name": "ExtractTablesFromHTML",
            "task": "Pull out table data from HTML as rows. Return {\"tables\": [[[\"cell1\", \"cell2\"]]]} (a list of tables)."
        },
        {
            "name": "MarkdownToHTML",
            "task": "Convert Markdown text into HTML. Return {\"html\": \"...\"}."
        },
        {
            "name": "ExtractCodeSections",
            "task": "Find code blocks in text. Return {\"code_blocks\": [\"...\"]}."
        },
        {
            "name": "TransformHrDocToJSON",
            "task": "Parse an HR document, mapping each heading to a JSON key. Return {\"hr_structure\": {\"Heading1\": \"...\"}}."
        },
        {
            "name": "NamedEntityPairExtraction",
            "task": "Return pairs of named entities found in the text. Return {\"entity_pairs\": [[\"EntityA\", \"EntityB\"], ...]}."
        },
        {
            "name": "SummaryToBulletList",
            "task": "Split a summary into bullet points at sentence boundaries. Return {\"bullet_points\": [\"...\"]}."
        },
        {
            "name": "ParseMLACitation",
            "task": "Extract authors, title, publication info from an MLA citation. Return {\"citation\": {\"authors\": \"...\", \"title\": \"...\", ...}}."
        },
        {
            "name": "UnifyMeasurementUnits",
            "task": "Scan for measurements and normalize them to a standard system. Return {\"normalized_text\": \"...\"}."
        },
        {
            "name": "ExtractJobTitles",
            "task": "Identify job titles from a resume or CV text. Return {\"job_titles\": [\"...\"]}."
        },
        {
            "name": "TransformAppReviewsToJSON",
            "task": "Parse lines of app reviews into structured JSON. Return [{\"review\": \"...\", \"rating\": \"...\"}, ...]."
        },
        {
            "name": "ParseRecipeInstructions",
            "task": "Extract ingredients and steps from a recipe text. Return {\"ingredients\": [\"...\"], \"steps\": [\"...\"]}."
        },
        {
            "name": "CoordinatesExtractor",
            "task": "Pull out lat/long if found. Return {\"coordinates\": [lat, long]} or {\"coordinates\": null} if none."
        },
        {
            "name": "StructureForumPosts",
            "task": "Convert forum text lines into structured fields (title, author, etc.). Return a list of objects: [{\"title\": \"...\", \"author\": \"...\"}]."
        },
        {
            "name": "KeywordsWithFrequencies",
            "task": "Extract repeated keywords and their counts. Return {\"keyword_counts\": {\"keyword\": number, ...}}."
        },
        {
            "name": "ParseMusicPlaylistDescription",
            "task": "Pull out track names or artists from a playlist text. Return {\"tracks\": [\"...\"]}."
        },
        {
            "name": "TransformChatTranscriptToJSON",
            "task": "Create a conversation structure with speaker, message, timestamp. Return a list of messages: [{\"speaker\": \"...\", \"message\": \"...\", \"time\": \"...\"}]."
        },
        {
            "name": "ExtractCommonPhrasesAcrossDocs",
            "task": "Find recurring phrases across multiple documents. Return {\"common_phrases\": [\"...\"]}."
        },
        {
            "name": "DocToOutline",
            "task": "Organize text by its headings into an outline. Return {\"outline\": [\"Heading1: details\", \"Heading2: details\"]}."
        },
        {
            "name": "RewriteToSchema",
            "task": "Parse text and map data to each specified schema field. Return {\"schema\": {\"field1\": \"...\", \"field2\": \"...\"}}."
        },
        {
            "name": "ParseMathExpressions",
            "task": "Extract math formulas from text. Return {\"expressions\": [\"...\"]}."
        },
        {
            "name": "StandardizeAddressFormat",
            "task": "Map a messy address block into a standardized format. Return {\"address\": {\"street\": \"...\", \"city\": \"...\", \"zip\": \"...\"}}."
        },
        {
            "name": "HighlightAndAnnotate",
            "task": "Find key sentences and annotate them with metadata. Return {\"annotations\": [{\"text\": \"...\", \"note\": \"...\"}]}."
        },
        {
            "name": "PhoneNumbersFromLogs",
            "task": "Extract phone numbers from logs. Return {\"phone_numbers\": [\"...\"]}."
        },
        {
            "name": "CombineAndDeduplicateRecords",
            "task": "Merge records describing the same entity into one. Return a new list of unique records."
        },
        {
            "name": "TransformXMLToJSON",
            "task": "Parse XML data into an equivalent JSON structure. Return {\"json_data\": {...}}."
        },
        {
            "name": "ExtractHyperlinks",
            "task": "Find all hyperlink URLs in HTML. Return {\"links\": [\"...\"]}."
        },
        {
            "name": "MentionExtraction",
            "task": "Extract user mentions from text (e.g. @username). Return {\"mentions\": [\"...\"]}."
        },
        {
            "name": "TransformParagraphsToList",
            "task": "Split a block of text into paragraphs. Return {\"paragraphs\": [\"...\", \"...\"]}."
        },
        {
            "name": "ParseLogEntriesToFields",
            "task": "Split log lines into structured fields (date, severity, message). Return a list of objects, each with these fields."
        },
        {
            "name": "CodeDocstringExtractor",
            "task": "Find docstrings or comments in source code. Return {\"docstrings\": [\"...\"]}."
        },

        # 4) QUESTION ANSWERING & CONTEXT RETRIEVAL (36 Tasks)
        {
            "name": "AnswerFactualQuestion",
            "task": "Quickly answer a direct question using the provided context. Return {\"answer\": \"...\"}."
        },
        {
            "name": "RetrieveDefinitionOfTerm",
            "task": "Look up a term's definition in some reference text. Return {\"definition\": \"...\"}."
        },
        {
            "name": "FindSpecificStatistic",
            "task": "Search for a numeric stat in data text. Return {\"statistic\": \"...\"}."
        },
        {
            "name": "MultiPartQuestionAnswering",
            "task": "Answer multiple related questions from a single block of context. Return {\"answers\": [\"...\"]}."
        },
        {
            "name": "HypothesizePossibleAnswers",
            "task": "Generate potential answers from multiple partial contexts. Return {\"possible_answers\": [\"...\"]}."
        },
        {
            "name": "LawQuestionAnswer",
            "task": "Provide a direct legal Q&A based on provided statutes or doc. Return {\"legal_answer\": \"...\"}."
        },
        {
            "name": "AnswerWithQuotes",
            "task": "Give an answer plus a verbatim quote from context. Return {\"answer\": \"...\", \"quote\": \"...\"}."
        },
        {
            "name": "FindRelevantSection",
            "task": "Locate the paragraph in the document that best answers the question. Return {\"relevant_section\": \"...\"}."
        },
        {
            "name": "RankBestAnswers",
            "task": "Score candidate answers' relevance. Return a list of (answer, score). E.g. {\"ranked_answers\": [[\"Answer1\", 0.9], [\"Answer2\", 0.7]]}."
        },
        {
            "name": "TriviaQuestionSolver",
            "task": "Provide a concise answer to a trivia question. Return {\"trivia_answer\": \"...\"}."
        },
        {
            "name": "HighlightConfidenceAnswer",
            "task": "Return an answer and a confidence score. E.g. {\"answer\": \"...\", \"confidence\": 0.85}."
        },
        {
            "name": "NestedQA",
            "task": "Split a large doc into sections, search each, merge partial answers. Return {\"answer\": \"...\"}."
        },
        {
            "name": "FillInTheBlank",
            "task": "Complete a partially written prompt. Return {\"completion\": \"...\"}."
        },
        {
            "name": "HistoricalFactFinder",
            "task": "Answer a question specifically about historical data. Return {\"historical_answer\": \"...\"}."
        },
        {
            "name": "ContextDrivenFAQ",
            "task": "Select the best FAQ entry or synthesize a new one. Return {\"faq_answer\": \"...\"}."
        },
        {
            "name": "StepByStepSolution",
            "task": "Provide a multi-step reasoning chain. Return {\"detailed_solution\": \"...\"}."
        },
        {
            "name": "CodeDebugQA",
            "task": "Answer a question about code behavior or bugs. Return {\"debug_answer\": \"...\"}."
        },
        {
            "name": "LogicPuzzleSolver",
            "task": "Solve a short logic puzzle. Return {\"solution\": \"...\"}."
        },
        {
            "name": "HighlightAllPossibleAnswers",
            "task": "Find every snippet in the doc that might answer a complex query. Return {\"snippets\": [\"...\"]}."
        },
        {
            "name": "ConflictingAnswerHandler",
            "task": "Check multiple sources for contradictory answers. Return {\"conflicts\": {\"source1\": \"answer1\", \"source2\": \"answer2\"}}."
        },
        {
            "name": "FactualEvidenceCitation",
            "task": "Answer and cite the text part that supports the conclusion. Return {\"answer\": \"...\", \"citation\": \"...\"}."
        },
        {
            "name": "YesNoMaybeQuestion",
            "task": "Return 'yes', 'no', or 'maybe' with a short justification. {\"response\": \"yes\", \"justification\": \"...\"}."
        },
        {
            "name": "MultiContextFusionAnswer",
            "task": "Fuse multiple contexts into one comprehensive answer. Return {\"fusion_answer\": \"...\"}."
        },
        {
            "name": "ShortAnswerCompletion",
            "task": "Supply a concise answer ignoring extended detail. Return {\"short_answer\": \"...\"}."
        },
        {
            "name": "EssayQuestionWriter",
            "task": "Generate an in-depth explanation from references. Return {\"essay\": \"...\"}."
        },
        {
            "name": "FillMissingInfo",
            "task": "Retrieve data for each missing field from context. E.g. {\"field1\": \"value\", \"field2\": \"value\"}."
        },
        {
            "name": "LocationBasedQuery",
            "task": "Answer a location-based query (addresses, directions). Return {\"location_answer\": \"...\"}."
        },
        {
            "name": "DirectQuotePassage",
            "task": "Return the exact excerpt from the doc that best addresses the question. {\"quoted_passage\": \"...\"}."
        },
        {
            "name": "PolicyManualAnswer",
            "task": "Consult policy text to produce a relevant answer. Return {\"policy_answer\": \"...\"}."
        },
        {
            "name": "ShortDefinitionLookup",
            "task": "Find a short definition from a glossary. Return {\"definition\": \"...\"}."
        },
        {
            "name": "MultiDocReference",
            "task": "Attempt to answer from each document. Return a mapping doc->answer: {\"doc1\": \"answer\", \"doc2\": \"answer\"}."
        },
        {
            "name": "CorrectCommonMisconceptions",
            "task": "Answer while clarifying typical misconceptions. Return {\"explanation\": \"...\"}."
        },
        {
            "name": "NumericAnswerExtractor",
            "task": "Parse a numeric answer from the data. Return {\"value\": number} e.g. {\"value\": 42.0}."
        },
        {
            "name": "InstructiveHowTo",
            "task": "Generate stepwise instructions for a 'how-to' question. Return {\"steps\": [\"Step1\", \"Step2\"]}."
        },
        {
            "name": "FormulaDerivationQA",
            "task": "Walk through deriving or applying a math formula. Return {\"formula_solution\": \"...\"}."
        },
        {
            "name": "UnifyMultipleAnswers",
            "task": "Merge partial answers from different sources into one. Return {\"unified_answer\": \"...\"}."
        },

        # 5) TEXT GENERATION & CREATIVE WRITING (36 Tasks)
        {
            "name": "GeneratePoem",
            "task": "Create a poem about a given theme/style. Return {\"poem\": \"...\"}."
        },
        {
            "name": "ShortStoryWriter",
            "task": "Produce a short fictional narrative within a word limit. Return {\"story\": \"...\"}."
        },
        {
            "name": "GenerateBrandTagline",
            "task": "Generate a catchy brand tagline. Return {\"tagline\": \"...\"}."
        },
        {
            "name": "StylizedMotivationalQuote",
            "task": "Compose a motivational quote in a specific style or tone. Return {\"quote\": \"...\"}."
        },
        {
            "name": "ComedicParodySketch",
            "task": "Write a short comedic parody of a given scenario. Return {\"parody\": \"...\"}."
        },
        {
            "name": "RewriteInShakespeareanEnglish",
            "task": "Transform text (or a concept) into a Shakespearean style. Return {\"shakespearean_text\": \"...\"}."
        },
        {
            "name": "ChildrenStoryWithMoral",
            "task": "Generate a brief children's story teaching a moral lesson. Return {\"story\": \"...\"}."
        },
        {
            "name": "FuturisticSciFiScene",
            "task": "Create a scene set in a futuristic sci-fi world. Return {\"scene\": \"...\"}."
        },
        {
            "name": "RomanceMiniPlotSetup",
            "task": "Draft the outline of a romantic story with a key conflict. Return {\"plot_outline\": \"...\"}."
        },
        {
            "name": "ComedicDialogueSketch",
            "task": "Write a humorous dialogue between specified characters. Return {\"dialogue\": \"...\"}."
        },
        {
            "name": "FableCreationWithAnimals",
            "task": "Write a short fable featuring talking animals and a moral. Return {\"fable\": \"...\"}."
        },
        {
            "name": "ShortHaiku",
            "task": "Compose a 17-syllable haiku on a given topic. Return {\"haiku\": \"...\"}."
        },
        {
            "name": "SpeechForSpecialEvent",
            "task": "Draft a brief speech for a wedding, graduation, etc. Return {\"speech\": \"...\"}."
        },
        {
            "name": "RewriteAsEpicSaga",
            "task": "Expand a snippet into an epic heroic saga. Return {\"epic_saga\": \"...\"}."
        },
        {
            "name": "HistoricalAlternateRealityScene",
            "task": "Write a scene that re-imagines a historical event differently. Return {\"alternate_history\": \"...\"}."
        },
        {
            "name": "HumorizeText",
            "task": "Make text comedic by adding humorous twists. Return {\"comedic_version\": \"...\"}."
        },
        {
            "name": "HorrorMicroStory",
            "task": "Create a very short horror story from a prompt. Return {\"horror_story\": \"...\"}."
        },
        {
            "name": "FairyTaleEndingGenerator",
            "task": "Generate a classic 'fairy tale' resolution from a conflict scenario. Return {\"fairy_tale_ending\": \"...\"}."
        },
        {
            "name": "PuzzleRiddleGenerator",
            "task": "Create a riddle or puzzle around a given topic. Return {\"riddle\": \"...\"}."
        },
        {
            "name": "RewriteAsDystopianIntro",
            "task": "Transform text into a dystopian opening paragraph. Return {\"dystopian_intro\": \"...\"}."
        },
        {
            "name": "ComedicInsultGenerator",
            "task": "Generate playful, mild comedic insults. Return {\"insult\": \"...\"}."
        },
        {
            "name": "PirateStyleTranslation",
            "task": "Rewrite text with pirate expressions ('Ahoy', 'Matey'). Return {\"pirate_text\": \"...\"}."
        },
        {
            "name": "RewriteWithSarcasticTone",
            "task": "Convert neutral text into a sarcastic version. Return {\"sarcastic_text\": \"...\"}."
        },
        {
            "name": "ImagineAlienDialogue",
            "task": "Create a dialogue between alien beings on a new planet. Return {\"alien_dialogue\": \"...\"}."
        },
        {
            "name": "ComedicProductReview",
            "task": "Write a humorous ad-style review for a product. Return {\"comedic_review\": \"...\"}."
        },
        {
            "name": "FreestyleRapLyrics",
            "task": "Generate rap lyrics about a topic. Return {\"rap_lyrics\": \"...\"}."
        },
        {
            "name": "ComedicObituaryPrompt",
            "task": "Satirically write a comedic obituary (lighthearted). Return {\"obituary\": \"...\"}."
        },
        {
            "name": "CondescendingPersuasion",
            "task": "Rewrite text as if persuading someone from a superior vantage point (in a humorous tone). Return {\"condescending_version\": \"...\"}."
        },
        {
            "name": "RewriteAsIfSpokenByRobot",
            "task": "Add mechanical, robotic speech patterns. Return {\"robot_text\": \"...\"}."
        },
        {
            "name": "KidsJokeGenerator",
            "task": "Create a family-friendly joke about a given topic. Return {\"kids_joke\": \"...\"}."
        },
        {
            "name": "ActionSceneDescription",
            "task": "Generate an intense, cinematic action scene. Return {\"action_scene\": \"...\"}."
        },
        {
            "name": "MonologueForVillain",
            "task": "Write a dramatic villain monologue. Return {\"villain_monologue\": \"...\"}."
        },
        {
            "name": "ComedicAutoReplyEmail",
            "task": "Generate a funny out-of-office auto-reply. Return {\"auto_reply\": \"...\"}."
        },
        {
            "name": "LivingObjectAnthropomorphicStory",
            "task": "Write a short narrative as if told by an inanimate object. Return {\"object_story\": \"...\"}."
        },
        {
            "name": "RewriteIntoSongChorus",
            "task": "Transform text into lyric chorus in a specified music genre. Return {\"chorus\": \"...\"}."
        },
        {
            "name": "CrossOverFanFiction",
            "task": "Create a short piece merging characters from different universes. Return {\"fan_fiction\": \"...\"}."
        },

        # 6) ANALYTICS & DATA INSIGHTS (36 Tasks)
        {
            "name": "BasicSentimentStats",
            "task": "Count how many texts are positive, negative, or neutral. Return percentages: {\"positive\": %, \"negative\": %, \"neutral\": %}."
        },
        {
            "name": "TopNWords",
            "task": "Identify the N most frequent words in the text. Return {\"top_words\": [\"word1\", \"word2\"]}."
        },
        {
            "name": "AverageSentenceLength",
            "task": "Compute the mean sentence length. Return {\"avg_sentence_length\": number}."
        },
        {
            "name": "NGramFrequency",
            "task": "Find frequencies of n-grams in a text. Return {\"ngrams\": {\"some n-gram\": count, ...}}."
        },
        {
            "name": "ReadingLevelEstimation",
            "task": "Estimate reading level from word complexity, etc. Return {\"reading_level\": \"...\"} (e.g. 'Grade 9')."
        },
        {
            "name": "StanceAnalysis",
            "task": "Count how many texts are pro, against, or neutral on an issue. Return {\"pro\": number, \"against\": number, \"neutral\": number}."
        },
        {
            "name": "TimelineOfEvents",
            "task": "Identify chronological references and place them in order. Return {\"events\": [{\"date\": \"...\", \"description\": \"...\"}]}."
        },
        {
            "name": "CorrelationOfKeywords",
            "task": "Show how often given keywords appear together. Return {\"co_occurrences\": {(\"keyword1\", \"keyword2\"): 10, ...}}."
        },
        {
            "name": "AverageParagraphComplexity",
            "task": "Compute average complexity per paragraph. Return {\"complexity_score\": number}."
        },
        {
            "name": "MultiDocumentTopicModeling",
            "task": "Discover main topics across multiple docs. Return {\"topics\": {\"topicA\": [docIndices], \"topicB\": [docIndices]}}."
        },
        {
            "name": "TfIdfRanking",
            "task": "Calculate TF-IDF for given terms. Return {\"tfidf_scores\": {\"term1\": number, \"term2\": number}}."
        },
        {
            "name": "CompareReviewScores",
            "task": "Compute avg rating by category from (text, score) pairs. Return {\"averages\": {\"categoryA\": number, \"categoryB\": number}}."
        },
        {
            "name": "IdentifyOutliersInTextLengths",
            "task": "Find abnormally long or short docs among many. Return {\"outliers\": [doc indices or IDs]}."
        },
        {
            "name": "PositivityVsNegativityTrend",
            "task": "Calculate positivity ratio for each item, track over time. Return e.g. {\"trend\": [ {\"index\": 1, \"ratio\": 0.8}, ... ]}."
        },
        {
            "name": "ComputeSyntacticDiversity",
            "task": "Estimate how varied the syntax is. Return {\"syntactic_diversity\": number}."
        },
        {
            "name": "MeasureRepetitivePhrases",
            "task": "Count repeated phrases throughout text. Return {\"repetitions\": {\"phrase\": count, ...}}."
        },
        {
            "name": "DetectReadabilityDropOff",
            "task": "Flag paragraphs too dense or complex. Return {\"difficult_paragraphs\": [indexes]}."
        },
        {
            "name": "ProgressiveToneAnalysis",
            "task": "Track how tone changes from one text to the next. Return {\"tone_progression\": [\"neutral\", \"positive\", ...]}."
        },
        {
            "name": "GatherEntityFrequencyAcrossDocs",
            "task": "Count how often each known entity is mentioned across docs. Return {\"entity_counts\": {\"Entity1\": number, ...}}."
        },
        {
            "name": "CompareHeadersAcrossDocuments",
            "task": "Check which docs contain which headings. Return {\"headingA\": [true/false per doc], ...}."
        },
        {
            "name": "TrackPolarizingKeywords",
            "task": "Count occurrences of loaded terms in a corpus. Return {\"keyword_counts\": {\"keyword\": number}}."
        },
        {
            "name": "SummarizeFeedbackTrends",
            "task": "Analyze overall sentiment and common themes in feedback. Return {\"summary\": \"...\"}."
        },
        {
            "name": "StoryArcDetection",
            "task": "Identify exposition, climax, resolution segments in a story. Return {\"story_arc\": [\"exposition at paragraph X\", \"climax at paragraph Y\"]}."
        },
        {
            "name": "AggregatedEmotionHistogram",
            "task": "Generate a histogram of emotional categories. Return {\"emotion_histogram\": {\"joy\": count, \"anger\": count, ...}}."
        },
        {
            "name": "ConflictingOpinionExtractor",
            "task": "Find pairs of contradictory statements. Return {\"conflicts\": [[\"statement1\", \"statement2\"], ...]}."
        },
        {
            "name": "AdvancedKeywordContextMap",
            "task": "Store context windows around keywords. Return {\"keyword_context\": {\"keyword\": [\"context snippet1\", \"snippet2\"]}}."
        },
        {
            "name": "PerformanceReviewInsight",
            "task": "Identify recurring compliments/criticisms from performance reviews. Return {\"compliments\": [\"...\"], \"criticisms\": [\"...\"]}."
        },
        {
            "name": "BrandPerceptionAnalysis",
            "task": "Calculate brand sentiment or loyalty from text. Return {\"brand_sentiment\": {\"sentiment_score\": number, \"notes\": \"...\"}}."
        },
        {
            "name": "CompetitorMentionsFrequency",
            "task": "Count references to each competitor. Return {\"competitor_counts\": {\"CompetitorA\": number, \"CompetitorB\": number}}."
        },
        {
            "name": "StoryCohesionScore",
            "task": "Score how logically coherent a narrative is. Return {\"cohesion_score\": number}."
        },
        {
            "name": "AdvancedSpellingAndGrammarStats",
            "task": "Count grammar/spelling errors. Return {\"error_counts\": {\"spelling\": number, \"grammar\": number}, \"score\": number}."
        },
        {
            "name": "FragmentationAnalysis",
            "task": "Measure how frequently the text changes topic or viewpoint. Return {\"fragmentation_score\": number}."
        },
        {
            "name": "RepeatedQuestionDetection",
            "task": "List any repeated questions in a text. Return {\"repeated_questions\": [\"...\"]}."
        },
        {
            "name": "MultiAuthorTextAnalysis",
            "task": "Analyze style features to see how each segment might differ by author. Return e.g. {\"segment_analysis\": {1: {\"vocab_richness\": number, ...}, 2: {...}}}."
        },
        {
            "name": "MeasureLinguisticStyleShift",
            "task": "Score how different two texts are in style/vocabulary. Return {\"style_diff_score\": number}."
        },
        {
            "name": "ConversationTurnAnalysis",
            "task": "Count how many times each participant speaks and average turn length. Return {\"turn_data\": {\"Participant1\": {\"turns\": x, \"avg_length\": y}}}."
        },

        # 7) USER INTERACTION & COMMUNICATION TASKS (36 Tasks)
        {
            "name": "GeneratePersonalizedEmailGreeting",
            "task": "Create a warm, personal greeting for an email. Return {\"greeting\": \"...\"}."
        },
        {
            "name": "ComposeCustomerSupportEmail",
            "task": "Draft a polite response explaining steps to resolve the user's issue. Return {\"support_email\": \"...\"}."
        },
        {
            "name": "RewriteInBriefTextMessageForm",
            "task": "Condense a paragraph into a short text message. Return {\"text_message\": \"...\"}."
        },
        {
            "name": "GenerateFormalApologyEmail",
            "task": "Create a formal apology letter for a mistake. Return {\"apology_email\": \"...\"}."
        },
        {
            "name": "AppointmentReminderMessage",
            "task": "Generate a short, friendly reminder of an upcoming appointment. Return {\"reminder_message\": \"...\"}."
        },
        {
            "name": "ReRankHelpArticles",
            "task": "Sort help articles by relevance to a user’s query. Return a new ordered list of articles: {\"re_ranked\": [article1, ...]}."
        },
        {
            "name": "PrioritizeCustomerQueries",
            "task": "Order user queries from highest to lowest priority. Return {\"sorted_queries\": [\"...\"]}."
        },
        {
            "name": "MeetingAgendaGenerator",
            "task": "Create a structured meeting agenda with relevant points. Return {\"agenda\": \"...\"}."
        },
        {
            "name": "FormalAnnouncementDraft",
            "task": "Take details and produce a polished announcement. Return {\"announcement\": \"...\"}."
        },
        {
            "name": "JobOfferLetter",
            "task": "Write a formal job offer letter with position, salary, etc. Return {\"offer_letter\": \"...\"}."
        },
        {
            "name": "ReorderSupportTickets",
            "task": "Sort tickets based on policy for severity. Return {\"sorted_tickets\": [...]}."
        },
        {
            "name": "UserFeedbackAutoReply",
            "task": "Generate a quick response thanking a user for feedback. Return {\"auto_reply\": \"...\"}."
        },
        {
            "name": "MarketingEmailForNewFeature",
            "task": "Write a promotional email about a new product feature. Return {\"marketing_email\": \"...\"}."
        },
        {
            "name": "InvoiceReminderEmail",
            "task": "Draft a friendly invoice payment reminder. Return {\"reminder_email\": \"...\"}."
        },
        {
            "name": "InternalUpdateMessage",
            "task": "Compose a short Slack/Teams update for a specific team. Return {\"update_message\": \"...\"}."
        },
        {
            "name": "UserEscalationHandler",
            "task": "Draft a calm, solution-oriented response to a user escalation. Return {\"escalation_response\": \"...\"}."
        },
        {
            "name": "ResumeCoverLetterTemplate",
            "task": "Generate a cover letter skeleton for a job application. Return {\"cover_letter\": \"...\"}."
        },
        {
            "name": "ProductReturnApprovalEmail",
            "task": "Write a formal notice approving a product return. Return {\"return_approval\": \"...\"}."
        },
        {
            "name": "WorkshopInvitation",
            "task": "Construct an invitation for a workshop (date, location, RSVP). Return {\"invitation\": \"...\"}."
        },
        {
            "name": "UserOnboardingInstructions",
            "task": "Generate a step-by-step welcome message for a new user. Return {\"onboarding_guide\": \"...\"}."
        },
        {
            "name": "PoliteMeetingRescheduleEmail",
            "task": "Request to reschedule a meeting, explaining briefly. Return {\"reschedule_email\": \"...\"}."
        },
        {
            "name": "ReRankContactMethods",
            "task": "Order ways to contact a user by preference and effectiveness. Return {\"ranked_methods\": [\"method1\", \"method2\"]}."
        },
        {
            "name": "DailyBulletinAnnouncement",
            "task": "Summarize daily internal news items. Return {\"bulletin\": \"...\"}."
        },
        {
            "name": "PersonalizedFollowupEmail",
            "task": "A follow-up referencing a previous conversation/event. Return {\"followup_email\": \"...\"}."
        },
        {
            "name": "ReRankAppNotifications",
            "task": "Sort notifications so the user sees the most critical first. Return {\"notifications\": [...]} with new order."
        },
        {
            "name": "VolunteerRecruitmentMessage",
            "task": "Draft a call-to-action asking for event volunteers. Return {\"recruitment_email\": \"...\"}."
        },
        {
            "name": "WriteCongratulatoryNote",
            "task": "Compose a short note congratulating someone on a milestone. Return {\"congrats_note\": \"...\"}."
        },
        {
            "name": "ReRankForumQuestions",
            "task": "Order forum questions by relevance to user interests. Return {\"sorted_questions\": [\"...\"]}."
        },
        {
            "name": "ScheduleUpdateNotification",
            "task": "Summarize schedule changes and notify recipients. Return {\"update_notification\": \"...\"}."
        },
        {
            "name": "ReRankProductSearchResults",
            "task": "Sort or reorder product results by query relevance. Return {\"sorted_results\": [...]}."
        },
        {
            "name": "HolidayGreetingMessage",
            "task": "Create a festive greeting for a specified holiday. Return {\"greeting\": \"...\"}."
        },
        {
            "name": "ProjectKickoffEmail",
            "task": "Announce a new project with immediate action items. Return {\"kickoff_email\": \"...\"}."
        },
        {
            "name": "AutoThankYouForFeedback",
            "task": "Generate an automated thank-you for feedback. Return {\"thank_you\": \"...\"}."
        },
        {
            "name": "CodeOfConductReminder",
            "task": "Remind a group about code of conduct/policy guidelines. Return {\"reminder\": \"...\"}."
        },
        {
            "name": "SponsorRenewalRequestEmail",
            "task": "Invite a sponsor to renew their support for an event. Return {\"renewal_request\": \"...\"}."
        },
        {
            "name": "NextStepsFollowupAfterMeeting",
            "task": "Draft a post-meeting follow-up with next steps and owners. Return {\"followup\": \"...\"}."
        }
    ]
    # Step 2: Initialize the LearnSkill
    learner = LearnSkill(model_name="gpt-4o-mini", verbose=True)

    for i, task in enumerate(tasks):
        # Step 4: Learn the skill with the defined task
        skill = learner.learn_skill(
            [],
            task=task['task'],
            model_name="gpt-4o-mini",
        )

        skill.save(f'{task['name']}.json')
        print(f'Processed {i}, {task["name"]}')


if __name__ == "__main__":
    main()