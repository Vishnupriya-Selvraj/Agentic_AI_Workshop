from agent import ResearchAgent

def main():
    topic = input("🔍 Enter a research topic: ")
    agent = ResearchAgent(topic)

    print("🧠 Generating research questions...")
    agent.generate_questions()

    print("🌐 Searching web for answers...")
    agent.search_answers()

    print("📝 Compiling report...")
    agent.compile_report()

    filepath = agent.save_report()
    print(f"\n✅ Markdown report saved as '{filepath}'")

    pdf_path = agent.export_pdf()
    print(f"📄 PDF version saved as '{pdf_path}'")

if __name__ == "__main__":
    main()
