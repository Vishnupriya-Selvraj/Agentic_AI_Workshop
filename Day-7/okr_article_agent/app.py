import streamlit as st
import re
import requests
from typing import TypedDict, Optional
import google.generativeai as genai

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda

# ========== API Keys ==========
GEMINI_API_KEY = "AIzaSyDPKMNs9m7LmDijqZ_ARwML0HsPmljpCg4"  # ✅ Replace with your actual key
SERPER_API_KEY = "7c21f9740ae2633a467bb58ad046f82b7809e952"

# ========== Gemini Setup ==========
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# ========== State Schema ==========
class State(TypedDict):
    article: str
    tags: list[str]
    parsed: Optional[dict]
    plagiarism_score: Optional[int]
    quality_feedback: Optional[str]
    okr_score: Optional[int]
    matched_tags: Optional[list[str]]
    benchmark: Optional[str]
    benchmark_source: Optional[str]
    rephrased: Optional[str]

# ========== Agents ==========
def parse_article_fn(state: State) -> State:
    text = state["article"]
    headings = re.findall(r"(?m)^(#+\s.*|.*\n[-=]{3,})", text)
    word_count = len(text.split())
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()])

    prompt = f"Extract 5–10 relevant keywords from the following article:\n\n{text}"
    response = model.generate_content(prompt)
    keywords = response.text.strip()

    state["parsed"] = {
        "headings": headings,
        "keywords": keywords,
        "word_count": word_count,
        "paragraphs": paragraph_count
    }
    return state

def plagiarism_check_fn(state: State) -> State:
    text = state["article"]
    prompt = f"You are a plagiarism checker. Score the article's originality from 0–100. Respond with only the score.\n\n{text}"
    response = model.generate_content(prompt).text
    try:
        score = int(''.join(filter(str.isdigit, response)))
    except:
        score = 50
    state["plagiarism_score"] = max(0, min(score, 100))
    return state

def assess_quality_fn(state: State) -> State:
    prompt = "Evaluate the article for clarity, technical depth, and logical structure. Provide a short report.\n\n" + state["article"]
    response = model.generate_content(prompt).text
    state["quality_feedback"] = response
    return state

def okr_match_fn(state: State) -> State:
    text = state["article"]
    tags = state["tags"]
    matches = [tag for tag in tags if tag.lower() in text.lower()]
    score = int((len(matches) / len(tags)) * 100)
    state["okr_score"] = score
    state["matched_tags"] = matches
    return state

def benchmark_fn(state: State) -> State:
    title = state.get("title", "").strip()
    parsed = state.get("parsed", {})
    keywords = parsed.get("keywords", "").split(",") if parsed.get("keywords") else []
    topic = title or (keywords[0] if keywords else "Design Thinking")

    serp_url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": f"{topic} blog article"}

    res = requests.post(serp_url, headers=headers, json=payload).json()
    articles = res.get("organic", [])
    if not articles:
        state["benchmark"] = "No benchmark articles found."
        state["benchmark_source"] = ""
        return state

    best = articles[0]
    blog_title = best.get("title", "")
    snippet = best.get("snippet", "")
    url = best.get("link", "")

    prompt = f"""You are an academic summarizer. Expand and rephrase the following blog snippet as a high-quality benchmark article on '{topic}'.
Write at least 3 paragraphs covering key concepts, use cases, and takeaways. End with a source mention.

Title: {blog_title}
Snippet: {snippet}
URL: {url}
"""
    benchmark = model.generate_content(prompt).text
    state["benchmark"] = benchmark
    state["benchmark_source"] = url  # 🆕 Store source URL
    return state


def rephrase_fn(state: State) -> State:
    text = state["article"]
    prompt = f"Rephrase the following article to improve clarity, structure, and engagement:\n\n{text}"
    rephrased = model.generate_content(prompt).text
    state["rephrased"] = rephrased
    return state

# ========== Graph ==========
def build_graph():
    builder = StateGraph(State)
    builder.add_node("parser", RunnableLambda(parse_article_fn))
    builder.add_node("plagiarism", RunnableLambda(plagiarism_check_fn))
    builder.add_node("quality", RunnableLambda(assess_quality_fn))
    builder.add_node("okr", RunnableLambda(okr_match_fn))
    builder.add_node("benchmark_gen", RunnableLambda(benchmark_fn))
    builder.add_node("rephrase", RunnableLambda(rephrase_fn))

    builder.set_entry_point("parser")
    builder.add_edge("parser", "plagiarism")
    builder.add_edge("plagiarism", "quality")
    builder.add_edge("quality", "okr")
    builder.add_edge("okr", "benchmark_gen")
    builder.add_edge("benchmark_gen", "rephrase")
    builder.set_finish_point("rephrase")

    return builder.compile()

# ========== Streamlit UI ==========
st.set_page_config(page_title="🧠 OKR Article Quality Evaluator", layout="wide")
st.title("🧠 OKR Article Quality Evaluator")
st.info("Paste your article and see how it aligns with OKRs, originality, clarity, and quality.")

title = st.text_input("📄 Article Title", placeholder="e.g., Design Thinking 101")
description = st.text_input("📝 Article Description", placeholder="e.g., Basics of Design Thinking with #snsinstitutions")
content = st.text_area("📖 Article Content", height=300, placeholder="Paste your article here...")

if st.button("🔍 Evaluate Article"):
    if not content:
        st.warning("Please include article content.")
    else:
        graph = build_graph()
        tags = ["#snsinstitutions", "#snsdesignthinkers", "#designthinking"]
        inputs = {"article": content, "tags": tags}

        with st.spinner("🔍 Evaluating article with AI agents..."):
            final_state = graph.invoke(inputs)

        st.header("📁 Structured Parsing (Agent 1)")
        parsed = final_state.get("parsed", {})
        st.write(f"**Headings:** {parsed.get('headings', []) or 'None found'}")
        st.write(f"**Keywords:** {parsed.get('keywords', '')}")
        st.write(f"**Word Count:** {parsed.get('word_count', 0)}")
        st.write(f"**Paragraph Count:** {parsed.get('paragraphs', 0)}")

        st.header("🧠 Originality & Clarity Evaluation (Agent 2)")
        st.metric("Plagiarism Score", f"{final_state.get('plagiarism_score', 0)} / 100")
        st.subheader("Feedback on Quality")
        st.info(final_state.get("quality_feedback", "N/A"))

        st.header("🎯 OKR Alignment (Agent 3)")
        st.metric("OKR Match Score", f"{final_state.get('okr_score', 0)} / 100")
        matched = final_state.get("matched_tags", [])
        st.write(f"**Matched Tags:** {', '.join(matched) if matched else 'None'}")

        st.header("🚀 Benchmark & Suggestions (Agent 4)")
        st.subheader("🌟 Example Benchmark Article")
        st.write(final_state.get("benchmark", "N/A"))
        source_url = final_state.get("benchmark_source", "")
        if source_url:
            st.markdown(f"🔗 **Source**: [View Original Article]({source_url})", unsafe_allow_html=True)  # 🆕

        st.subheader("🪄 Suggested Rephrasing")
        st.write(final_state.get("rephrased", "N/A"))

        st.header("📊 Final Score")
        overall = int((final_state.get("plagiarism_score", 0) + final_state.get("okr_score", 0)) / 2)
        st.metric("Overall Score", f"{overall} / 100")
