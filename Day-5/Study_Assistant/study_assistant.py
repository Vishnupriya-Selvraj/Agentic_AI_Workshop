import streamlit as st
import PyPDF2
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult
from langchain.chains import LLMChain
from typing import List, Optional
from pydantic import Field

# ----------- CONFIGURE GEMINI -----------
genai.configure(api_key="AIzaSyDPKMNs9m7LmDijqZ_ARwML0HsPmljpCg4")  # Replace with your Gemini API key
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ----------- Custom Gemini Wrapper -----------
class GeminiLLM(BaseLLM):
    model: any = Field(default=gemini_model)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        generations = []
        for prompt in prompts:
            output = self._call(prompt, stop=stop)
            generations.append([{"text": output}])
        return LLMResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        return "gemini"

llm = GeminiLLM()

# ----------- PDF Content Extraction -----------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# ----------- LangChain Prompts -----------
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Summarize the following educational content into key bullet points:

{text}

Summary in bullets:"""
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

quiz_prompt = PromptTemplate(
    input_variables=["summary", "num_questions"],
    template="""Generate {num_questions} multiple-choice questions (MCQs) based on the following summary. Each question should have 4 options (a–d) and clearly indicate the correct answer.

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
)
quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt)

# ----------- Streamlit UI -----------
st.set_page_config(page_title="📚 Study Assistant", layout="centered")
st.title("📚 AI Study Assistant - Quiz Generator")

st.markdown("Upload a **PDF** with study material. Then select how many MCQs you want to generate.")

uploaded_file = st.file_uploader("📄 Upload your study material (PDF)", type="pdf")
num_questions = st.number_input("❓ Number of Quiz Questions", min_value=1, max_value=50, value=10)

if uploaded_file:
    with st.spinner("🔍 Extracting content from PDF..."):
        raw_text = extract_text_from_pdf(uploaded_file)

    if not raw_text:
        st.error("⚠️ No text could be extracted. Please upload a readable PDF.")
        st.stop()

    st.success("✅ PDF content extracted.")
    st.text_area("📖 Extracted Content Preview", raw_text[:2000] + "...", height=300)

    if st.button("Generate Summary and MCQs"):
        with st.spinner("📝 Summarizing content..."):
            summary = summary_chain.run(text=raw_text)
            st.subheader("📌 Summary")
            st.markdown(summary)

        with st.spinner("🧪 Generating Quiz Questions..."):
            mcqs = quiz_chain.run(summary=summary, num_questions=str(num_questions))
            st.subheader(f"🎯 {num_questions} Quiz Questions")
            st.markdown(mcqs)
