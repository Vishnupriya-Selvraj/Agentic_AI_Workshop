import streamlit as st
import json
import requests

# ========== Constants ==========

OPENROUTER_API_KEY = "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"  # replace with your OpenRouter key

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "openai/gpt-3.5-turbo"

# ========== LLM Utilities ==========

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# ========== Agent Tasks ==========

def check_plagiarism(text):
    prompt = f"""You are a plagiarism checker. Score the following article's originality from 0–100 (100 means fully original, 0 means fully copied). 
Article: {text}
Respond with only the score."""
    response = ask_openrouter(prompt)
    try:
        score = int(''.join(filter(str.isdigit, response)))
        return max(0, min(score, 100))
    except:
        return 50  # default

def assess_quality(text):
    prompt = f"""Evaluate this article's clarity, technical depth, and structure. Provide qualitative feedback on:
1. Readability
2. Technical depth
3. Structure and logical flow"""
    return ask_openrouter(prompt)

def rephrase_text(text):
    prompt = f"""Rephrase the following article for better clarity and coherence:\n\n{text}"""
    return ask_openrouter(prompt)

def match_okrs(text, tags):
    matches = [tag for tag in tags if tag.lower() in text.lower()]
    score = int((len(matches) / len(tags)) * 100)
    return score, matches

def retrieve_benchmark(topic):
    prompt = f"""Provide a high-quality, original blog article example on the topic: {topic}"""
    return ask_openrouter(prompt)

# ========== Streamlit UI ==========

st.set_page_config(page_title="🧠 OKR Article Quality Evaluator", layout="wide")
st.title("🧠 OKR Article Quality Evaluator")
st.info("Enter article details below. Include hashtags such as #snsinstitutions, #snsdesignthinkers, #designthinking in the content.")

# ✅ Modified Input Section
title = st.text_input("📄 Article Title", placeholder="e.g., Design Thinking 101")
description = st.text_input("📝 Article Description", placeholder="e.g., Basics of Design Thinking")
content = st.text_area("📖 Article Content", height=300, placeholder="Paste your article here...")

if st.button("🔍 Evaluate Article"):
    if not content:
        st.warning("Please include article content.")
    else:
        st.success("Article parsed successfully!")

        st.subheader("📄 Title")
        st.write(title)

        st.subheader("📝 Description")
        st.write(description)

        st.subheader("📖 Content")
        st.write(content[:500] + ("..." if len(content) > 500 else ""))

        with st.spinner("🧬 Checking originality..."):
            plagiarism_score = check_plagiarism(content)

        with st.spinner("🧠 Assessing structure and depth..."):
            quality_feedback = assess_quality(content)

        okr_tags = ["#snsinstitutions", "#snsdesignthinkers", "#designthinking"]
        with st.spinner("🔗 Matching OKR Tags..."):
            okr_score, matched = match_okrs(content, okr_tags)

        with st.spinner("📖 Retrieving benchmark article..."):
            benchmark = retrieve_benchmark("Design Thinking")

        with st.spinner("✍️ Rephrasing for improvement..."):
            rephrased = rephrase_text(content)

        final_score = int((plagiarism_score + okr_score) / 2)

        # === OUTPUT ===
        st.header("📊 Evaluation Report")
        st.metric("Quality Score", f"{final_score} / 100")
        st.write(f"**Plagiarism Score:** {plagiarism_score}")
        st.write(f"**OKR Tag Match (%):** {okr_score}")
        st.write(f"**Matched Tags:** {', '.join(matched) if matched else 'None'}")

        st.subheader("🧠 LLM Feedback")
        st.info(quality_feedback)

        st.subheader("🪄 Suggested Rephrasing")
        st.write(rephrased)

        st.subheader("🌟 Benchmark Article")
        st.write(benchmark)
