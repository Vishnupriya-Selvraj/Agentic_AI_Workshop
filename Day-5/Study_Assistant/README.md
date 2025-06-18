📚 AI Study Assistant – Quiz Generator
An intelligent tool to help students and educators quickly generate summaries and custom quiz questions from uploaded PDF study materials using Google Gemini and LangChain.

🚀 Features
📄 Upload any PDF with educational content.

🧠 Extracts and summarizes key points using AI.

❓ Generates custom number of multiple-choice questions (MCQs).

🎯 Each MCQ includes 4 options with the correct answer clearly marked.

✅ Fully powered by LangChain + Google Gemini API.

🧰 Tech Stack
Python

Streamlit – UI Framework

LangChain – Prompt chaining and LLM integration

Google Generative AI (Gemini) – LLM backend

PyPDF2 – PDF parsing and text extraction

📝 Requirements
Install dependencies:

pip install -r requirements.txt
requirements.txt

streamlit
PyPDF2
google-generativeai
langchain
pydantic
🔑 Setup Instructions
Clone the Repository:

git clone https://github.com/your-username/study-assistant.git
cd study-assistant
Create a .env file or hardcode your Gemini API key:

GOOGLE_API_KEY=your_google_gemini_api_key
Or directly in code:

genai.configure(api_key="YOUR_API_KEY")
Run the App:

streamlit run study_assistant.py
💡 How It Works
Upload a PDF: The tool reads and extracts text from the file.

Summarization: It uses LangChain to prompt Gemini to summarize the content.

Quiz Generation: Based on the summary and your input (number of questions), the app generates MCQs in a standard format.

📸 UI Preview

📄 Upload PDF
❓ Select number of MCQs
📌 View AI-generated Summary
🎯 View auto-generated Quiz Questions
✨ Example MCQ Output

Question:
What is the function of the mitochondria?

a) Produces proteins  
b) Synthesizes DNA  
c) Generates energy  
d) Controls cell division  

Answer: c
✅ Goals Met
 Upload and extract content from PDF.

 Summarize educational content using LangChain prompt.

 Generate MCQs based on summary.

 Allow dynamic control over number of questions.

 Use LangChain for modular LLM logic.

 Streamlit UI for interactivity.
