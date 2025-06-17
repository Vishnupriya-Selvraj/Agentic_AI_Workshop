import streamlit as st
import PyPDF2
import google.generativeai as genai
from langchain.prompts import PromptTemplate

# ----------- CONFIGURE GEMINI -----------
genai.configure(api_key="AIzaSyDB70DqhUyE-wiclvgxJaXzz7mBEJc3mRM")

# Load Gemini Model
model = genai.GenerativeModel("gemini-pro")

# ----------- FUNCTION: Extract PDF Content -----------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# ----------- FUNCTION: Summarize Content -----------
def summarize_content(text):
    prompt = f"""Summarize the following educational content into key bullet points:

{text}

Summary in bullets:"""
    response = model.generate_content(prompt)
    return response.text

# ----------- FUNCTION: Generate Quiz Questions -----------
def generate_mcqs(summary):
    prompt = f"""Generate 3 multiple-choice questions (MCQs) based on the following summary. Each question should have 4 options (a-d) and clearly indicate the correct answer.

Summary:
{summary}

Format:
Question:
a) Option A
b) Option B
c) Option C
d) Option D
Answer: <correct option>

MCQs:"""
    response = model.generate_content(prompt)
    return response.text

# ----------- STREAMLIT UI -----------
st.set_page_config(page_title="📚 Study Assistant", layout="centered")
st.title("📚 AI Study Assistant - Quiz Generator")
st.markdown("Upload a **PDF** with study material, and this app will summarize it and generate MCQs.")

uploaded_file = st.file_uploader("Upload your study material (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("📄 Reading and extracting content from PDF..."):
        raw_text = extract_text_from_pdf(uploaded_file)

    st.success("✅ PDF content extracted.")
    st.text_area("Extracted Content", raw_text[:2000] + "...", height=300)

    if st.button("Generate Summary and MCQs"):
        with st.spinner("🧠 Summarizing content..."):
            summary = summarize_content(raw_text)
            st.subheader("📝 Summary")
            st.markdown(summary)

        with st.spinner("🧪 Generating Quiz Questions..."):
            mcqs = generate_mcqs(summary)
            st.subheader("❓ Quiz Questions")
            st.markdown(mcqs)
