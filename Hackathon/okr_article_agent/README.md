OKR ARTICLE QUALITY EVALUATOR
=============================

This is an AI-powered Streamlit app that evaluates the quality and originality of an article using a set of intelligent agents powered by GPT-3.5 via the OpenRouter API.

It is designed to help educational institutions, content teams, or quality evaluators assess OKR-based article submissions.

------------------------------------------------------------
FEATURES
------------------------------------------------------------

1. ✅ Plagiarism Detection
   - Scores originality from 0 to 100 using a GPT-based agent.

2. 📊 Quality Assessment
   - Evaluates clarity, technical depth, and structure.

3. 🔗 OKR Tag Matching
   - Scores how well the article aligns with hashtags like:
     #snsinstitutions, #snsdesignthinkers, #designthinking

4. ✍️ Rephrasing Agent
   - Improves clarity and coherence of the input article.

5. 🌟 Benchmark Article Generator
   - Provides a sample high-quality article on the same topic.

------------------------------------------------------------
API SOURCE
------------------------------------------------------------

🧠 OpenRouter API

Used to access GPT-3.5-turbo (or other LLMs).
Register here to get a free API key:
https://openrouter.ai

------------------------------------------------------------
REQUIREMENTS
------------------------------------------------------------

Python 3.8+

Install dependencies:

    pip install streamlit requests

------------------------------------------------------------
SETUP INSTRUCTIONS
------------------------------------------------------------

1. Clone the Repository:

    git clone https://github.com/yourusername/okr-article-evaluator.git
    cd okr-article-evaluator

2. Add Your OpenRouter API Key:

In `app.py`, update the following line:

    OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

(Alternatively, store it in an `.env` file for security)

3. Run the App:

    streamlit run app.py

4. Input Format:

Paste your article in the following JSON format:

    {
      "title": "Design Thinking 101",
      "description": "Basics of Design Thinking",
      "content": "Design Thinking is a process... #snsdesignthinkers #snsinstitutions #designthinking"
    }

------------------------------------------------------------
AGENTS (LLM-Powered)
------------------------------------------------------------

The app internally defines and uses 5 intelligent agents:

1. check_plagiarism(text)
   - Checks originality score (0–100)

2. assess_quality(text)
   - Provides feedback on clarity, depth, structure

3. match_okrs(text, tags)
   - Matches OKR hashtags and returns match %

4. retrieve_benchmark(topic)
   - Generates a high-quality sample article

5. rephrase_text(text)
   - Suggests improved version of article

All agents call the GPT model through OpenRouter API.

------------------------------------------------------------
PROJECT AUTHOR
------------------------------------------------------------

Developed by: Vishnupriya S G, SNSIHUB
Year: 2025

------------------------------------------------------------
