# 🌐 Web Research Agent using ReAct Pattern (Groq API + Tavily)

## 📘 Project Description
This project implements an intelligent web research agent that follows the **ReAct pattern (Reasoning + Acting)**. It automates research by:
- Generating intelligent research questions using **LLaMA-3 via Groq API**.
- Searching the web using the **Tavily API**.
- Compiling a structured **markdown report** from the results.

---

## 🧠 Core Architecture

### 🔹 ReAct Pattern
- **Reasoning Phase**: Plan the research process using a Large Language Model (LLaMA-3).
- **Acting Phase**: Execute the plan by searching the web and extracting relevant data.

### 🔧 Design Patterns Used
- **Planning Pattern**: Agent plans research via question generation.
- **Tool-Use Pattern**: Uses Groq (LLM) and Tavily (search tool).

---

## 🚀 Features
- 🔍 Topic-driven research automation.
- 🧠 LLaMA-3 via Groq API for generating deep, relevant questions.
- 🌐 Tavily API for fast, real-time search.
- 📄 Structured markdown report generation.
- 📦 Clean, modular Python code.

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/web-research-agent.git
cd web-research-agent
```
## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Setup .env file
Create a .env file in the root directory and add your API keys:

```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

🔑 Get Groq API key: https://console.groq.com
🔑 Get Tavily API key: https://docs.tavily.com

## 4. Run the agent

```bash
python main.py
```
You’ll be prompted to enter a topic. A structured markdown report will be saved as:

```bash
research_report.md
```