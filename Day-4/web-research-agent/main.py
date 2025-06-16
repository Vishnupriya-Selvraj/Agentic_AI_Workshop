from agent import ResearchAgent

def main():
    topic = input("🔍 Enter a research topic: ")
    agent = ResearchAgent(topic)

    print("🧠 Generating research questions...")
    agent.generate_questions()

    print("🌐 Searching web for answers...")
    agent.search_answers()

    print("📝 Compiling report...")
    report = agent.compile_report()

    with open("research_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n✅ Report saved as 'research_report.md'")

if __name__ == "__main__":
    main()
