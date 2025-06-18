# 🧠 OKR Article Quality Evaluator

A lightweight, multi-agent AI system built using [Streamlit](https://streamlit.io/), [LangGraph](https://github.com/langchain-ai/langgraph), and [Google Gemini](https://ai.google.dev/) that evaluates the quality of articles with respect to:

- ✅ Structure & Keyword Extraction  
- 🔍 Plagiarism Detection  
- 📈 Quality Assessment  
- 🎯 OKR Tag Matching  
- 🚀 Benchmark Generation  
- ✨ Rephrasing Suggestions

---

## 📦 Features

| Feature                    | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| 📖 Article Parsing        | Extracts headings, keywords, word count, and paragraph stats               |
| 🔎 Plagiarism Checker     | Gives originality score (0–100) using Gemini                               |
| 🧠 Quality Feedback       | Short summary on clarity, technical depth, and coherence                   |
| 🎯 OKR Matching           | Scores match with predefined organizational tags                           |
| 🏆 Benchmark Generator    | Uses Google Search (Serper.dev) to pull similar articles and generate a benchmark |
| ✍️ Rephrasing Agent       | Suggests a clearer and more engaging version of your article               |

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vishnupriya-Selvraj/Agentic_AI_Workshop/tree/main/Day-7/okr_article_agent
cd okr-article-evaluator
```

### 2. Set up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Create a .env File (Optional)

replace the following variables in the Python script directly:

```bash
GEMINI_API_KEY = "your-google-api-key"
SERPER_API_KEY = "your-serper-api-key"
```

## 📋 Requirements
Here are the key packages:

```bash
streamlit
requests
google-generativeai
langgraph
langchain-core
```

## Install via:

```bash
pip install streamlit requests google-generativeai langgraph langchain-core
```

## 🚀 Usage
Run the Streamlit app locally:
```bash
streamlit run app.py
```

You’ll be able to:

Enter article title, description, and content

Click Evaluate Article

View insights across:

Structured parsing

Plagiarism score

Quality feedback

OKR tag matches

Suggested benchmark

Suggested rephrasing

Final aggregated score

## 🧠 Architecture Overview
This project uses LangGraph to sequence multiple AI tasks (nodes):

```bash
graph TD;
    parser --> plagiarism;
    plagiarism --> quality;
    quality --> okr;
    okr --> benchmark;
    benchmark --> rephrase;
```
Each node runs a RunnableLambda using Gemini or an external API (e.g., Serper.dev for Google search).

## 🤖 Model Details

| Component        | Model Used            | Notes                                                                 |
|------------------|------------------------|-----------------------------------------------------------------------|
| Plagiarism       | `gemini-1.5-flash`     | Uses custom prompt to rate originality                                |
| Quality Feedback | `gemini-1.5-flash`     | Uses generative summary evaluation                                    |
| OKR Matching     | Internal logic         | Uses keyword overlap scoring                                          |
| Benchmark        | `gemini + serper.dev`  | Searches real articles, then uses Gemini to convert to academic style |
| Rephrasing       | `gemini-1.5-flash`     | Improves clarity, structure, and flow                                 |


## 🧪 Example Tags
The current tag list is:

```bash
tags = ["#snsinstitutions", "#snsdesignthinkers", "#designthinking"]
```

Update this list based on your OKRs or project-specific hashtags.
