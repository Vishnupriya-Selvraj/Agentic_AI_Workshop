# 🧠 OKR Article Quality Evaluator

An AI-powered Streamlit app that evaluates your article based on originality, OKR alignment, quality, benchmark comparison, and provides rephrasing suggestions to improve clarity and engagement.

---

## 🚀 Features

- ✅ **Structured Article Parsing**: Extracts headings, keywords, word/paragraph counts.
- 🔍 **Plagiarism Detection**: Gemini-based scoring of originality (0–100).
- ✨ **Quality Review**: Short, AI-generated feedback for improving writing quality.
- 🎯 **OKR Alignment Score**: Matches article description with specific hashtags.
- 📘 **Benchmark Suggestions**: Retrieves high-quality sample articles for reference.
- 🔁 **Rephrasing Agent**: Rewrites content to improve clarity and structure.
- 📊 **Overall Scoring**: Combines originality and OKR scores for a final result.

---

## 🛠️ Tech Stack

| Component         | Technology               |
|------------------|--------------------------|
| UI Framework     | Streamlit                |
| Language Model   | Google Gemini (1.5 Flash)|
| Embeddings       | Sentence Transformers    |
| Vector DB        | ChromaDB                 |
| Workflow Engine  | LangGraph + LangChain    |
| Search API       | Serper.dev               |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/okr-article-evaluator.git
cd okr-article-evaluator
2. Set Up Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
Example requirements.txt:

text
Copy code
streamlit
google-generativeai
chromadb
sentence-transformers
langchain
langgraph
🔐 Environment Variables
Create a .env file or set the keys directly in your script:

env
Copy code
GEMINI_API_KEY=your_google_gemini_api_key
SERPER_API_KEY=your_serper_api_key
You can get Serper API keys from serper.dev and Gemini keys from ai.google.dev.

▶️ Running the App
bash
Copy code
streamlit run app.py
This will launch the app in your browser.

✍️ Inputs Guide
📄 Article Title
Short headline for your content.

Example: Design Thinking for Beginners

📝 Description
A one-liner summary containing key OKR hashtags. These hashtags are used to calculate the alignment score:

#snsinstitutions

#snsdesignthinkers

#designthinking

Example: An intro to design principles and creativity. #snsinstitutions #designthinking

📖 Article Content
The full body of your article. Use markdown-style or underlined headings to help parsing.

✅ Recommended Formatting:
markdown
Copy code
# Introduction
Design thinking is a user-centered methodology...

## Stages
- Empathize
- Define
- Ideate
- Prototype
- Test

# Conclusion
It fosters creative solutions in real-world contexts.
📂 ChromaDB Benchmarking
Benchmarks are stored locally under ./chromadb_store/.

For each article topic, it searches a similar high-quality blog via Serper.dev and stores the generated content and URL.

Next time, similar topics load instantly from the DB.

🧠 Agents Workflow Overview
Agent	Task
parser	Extracts structure, headings, keywords
plagiarism	Estimates originality score via Gemini
quality	Gives clarity and structure feedback
okr	Checks if key hashtags exist in description
benchmark	Finds similar blog and generates reference content
rephrase	Rewrites article for clarity and impact

📊 Output
Sections:
✅ Headings, Keywords, Word/Paragraph Count

🧠 Originality Score + Quality Feedback

🎯 OKR Match Score + Matched Hashtags

📘 Benchmark Article (Generated)

🔁 Suggested Rephrasing

📈 Final Combined Score

🧪 Example Evaluation Flow
Paste your article title, description, and content.

App runs all agents sequentially via LangGraph.

Results are shown step-by-step, finishing with a final score.

🙋 FAQs
Q: What happens if my article lacks hashtags?
A: OKR match score will be low (0–100 is calculated based on matches in the description).

Q: Can I reuse benchmarked topics?
A: Yes! The app caches benchmarks locally using embeddings for faster retrieval.

Q: Can I deploy this app?
A: Yes, you can host it on Streamlit Cloud or deploy via any cloud server.

