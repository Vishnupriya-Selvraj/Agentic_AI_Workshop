import streamlit as st
import json
import requests
import re

# ========== Constants ==========

OPENROUTER_API_KEY = "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"  # Your OpenRouter Key
SERPER_API_KEY = "7c21f9740ae2633a467bb58ad046f82b7809e952"  # <-- Replace with your real Serper.dev API Key

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}
MODEL = "openai/gpt-3.5-turbo"

# ========== LLM Call Utility ==========

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# ========== Web Search (Serper.dev for Benchmarking) ==========

def web_search(query):
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()

# ========== RAG-based Benchmark Agent ==========

def retrieve_benchmark(topic):
    results = web_search(f"{topic} blog article")
    articles = results.get("organic", [])

    if not articles:
        return "No benchmark articles found."

    best_article = articles[0]
    title = best_article.get("title", "")
    snippet = best_article.get("snippet", "")
    link = best_article.get("link", "")

    full_prompt = f"""
You are an academic summarizer. Expand and rephrase the following blog snippet as a high-quality benchmark article on '{topic}'.
Write at least 3 paragraphs covering key concepts, use cases, and takeaways. End with a source mention.

Title: {title}
Snippet: {snippet}
URL: {link}
"""

    return ask_openrouter(full_prompt)

# ========== Article Parsing Agent ==========

def parse_article(text):
    headings = re.findall(r"(?m)^(#+\s.*|.*\n[-=]{3,})", text)
    word_count = len(text.split())
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()])

    keyword_prompt = f"""Extract 5–10 relevant keywords from the following article:\n\n{text}"""
    keywords = ask_openrouter(keyword_prompt)

    return {
        "headings": headings,
        "keywords": keywords,
        "word_count": word_count,
        "paragraphs": paragraph_count
    }

# ========== Originality & Quality ==========

def check_plagiarism(text):
    prompt = f"""You are a plagiarism checker. Score the article's originality from 0–100. Respond with only the score.\n\nArticle:\n{text}"""
    response = ask_openrouter(prompt)
    try:
        score = int(''.join(filter(str.isdigit, response)))
        return max(0, min(score, 100))
    except:
        return 50

def assess_quality(text):
    prompt = f"""Evaluate the article for clarity, technical depth, and logical structure. Provide a short report."""
    return ask_openrouter(prompt)

# ========== OKR Tag Matching ==========

def match_okrs(text, tags):
    matches = [tag for tag in tags if tag.lower() in text.lower()]
    score = int((len(matches) / len(tags)) * 100)
    return score, matches

# ========== Rephrase Agent ==========

def rephrase_text(text):
    prompt = f"""Rephrase the following article to improve clarity, structure, and engagement:\n\n{text}"""
    return ask_openrouter(prompt)

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
        with st.spinner("🔍 Parsing article..."):
            parsed_data = parse_article(content)

        with st.spinner("📚 Checking plagiarism..."):
            plagiarism_score = check_plagiarism(content)

        with st.spinner("🧠 Assessing clarity and depth..."):
            quality_feedback = assess_quality(content)

        okr_tags = ["#snsinstitutions", "#snsdesignthinkers", "#designthinking"]
        with st.spinner("🔗 Validating OKR alignment..."):
            okr_score, matched_tags = match_okrs(description, okr_tags)

        with st.spinner("🌐 Fetching & summarizing benchmark..."):
            benchmark = retrieve_benchmark(title or description or "Design Thinking")

        with st.spinner("✍️ Rephrasing for improvement..."):
            rephrased = rephrase_text(content)

        final_score = int((plagiarism_score + okr_score) / 2)

        # === OUTPUT ===
        st.header("📑 Structured Parsing (Agent 1)")
        st.write(f"**Headings:** {parsed_data['headings'] if parsed_data['headings'] else 'None found'}")
        st.write(f"**Keywords:** {parsed_data['keywords']}")
        st.write(f"**Word Count:** {parsed_data['word_count']}")
        st.write(f"**Paragraph Count:** {parsed_data['paragraphs']}")

        st.header("🧠 Originality & Clarity Evaluation (Agent 2)")
        st.metric("Plagiarism Score", f"{plagiarism_score} / 100")
        st.subheader("Feedback on Quality")
        st.info(quality_feedback)

        st.header("🎯 OKR Alignment (Agent 3)")
        st.metric("OKR Match Score", f"{okr_score} / 100")
        st.write(f"**Matched Tags:** {', '.join(matched_tags) if matched_tags else 'None'}")

        st.header("🚀 Benchmark & Suggestions (Agent 4)")
        st.subheader("🌟 Example Benchmark Article")
        st.write(benchmark)
        st.subheader("🪄 Suggested Rephrasing")
        st.write(rephrased)

        st.header("📊 Final Score")
        st.metric("Overall Score", f"{final_score} / 100")
