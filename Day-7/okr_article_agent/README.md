# 🧠 OKR Article Quality Evaluator

This Streamlit app helps evaluate written articles (especially student blogs or OKR-based content) on the following parameters:

- ✅ **Plagiarism detection** (Originality score)
- 🧠 **Clarity & quality assessment**
- 🎯 **OKR alignment** based on tags
- 🚀 **Benchmarking** against real-world blogs (via RAG with Serper.dev + LLM)
- ✍️ **Rephrasing suggestions**

---

## 🔧 Features

- Uses OpenRouter (ChatGPT API) to run LLM-powered tasks
- Uses Serper.dev (Google Search API) to fetch benchmark articles
- RAG (Retrieval-Augmented Generation) summarizes top blog articles on your topic
- Fully interactive with Streamlit UI

---

## 🚀 How to Run

1. **Clone the repo** or copy the code to a local folder:

   ```bash
   git clone <your-repo-url>
   cd <your-folder>
   ```

## Install dependencies:

```bash
pip install -r requirements.txt
```
Set your API keys in the code (app.py):

OPENROUTER_API_KEY: https://openrouter.ai

SERPER_API_KEY: https://serper.dev

Run the app:

```bash
streamlit run app.py
```

## 🔑 API Keys
OpenRouter: Get your key at https://openrouter.ai

Serper.dev: Get a free API key at https://serper.dev

## 📥 Input Example
Field	Example
Title	Design Thinking 101
Description	Basics of Design Thinking with #snsinstitutions
Content	# Introduction to Design Thinking\nDesign Thinking is...

## 📤 Output Example
✅ Headings, Keywords, Word Count

🔍 Plagiarism Score: 100 / 100

🧠 Quality Feedback: "Well-structured and informative..."

🎯 OKR Match Score: 100 / 100

🚀 Benchmark: Summarized blog with source reference

✍️ Rephrased Version of the Submitted Content

## 📦 Tech Stack
Python

Streamlit

OpenRouter API (LLM)

Serper.dev API (Search)