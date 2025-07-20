# Personalized Education Assistant (CrewAI)

## Overview
A sequential CrewAI-powered system that provides personalized educational recommendations for users. It generates learning materials tailored to user topics, creates quizzes, and suggests project ideas based on expertise level.

## Features
- **Learning Material Agent:** Curates videos, articles, and exercises for user topics.
- **Quiz Creator Agent:** Generates quizzes to test understanding.
- **Project Idea Agent:** Suggests practical project ideas based on expertise.
- **Custom Project Suggestion Tool:** Generates project ideas tailored to expertise and topics.
- **Structured Outputs:** Uses Pydantic models for learning materials, quizzes, and project ideas.

## Setup
1. **Clone the repository and navigate to the project directory:**
   ```sh
   git clone <your-repo-url>
   cd Personalized_Education_Assistant
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/Mac:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a `.env` file in the project root:**
   ```env
   SERPER_API_KEY=your_serper_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage
Run the main script:
```sh
python education_agents.py
```
You can modify the topics and expertise level in the `__main__` section.

## Output Structure
- **LearningMaterial:**
  - topic: str
  - videos: List[str]
  - articles: List[str]
  - exercises: List[str]
- **Quiz:**
  - topic: str
  - questions: List[QuizQuestion]
    - question: str
    - options: List[str]
    - answer: str
- **ProjectIdeas:**
  - topic: str
  - expertise: str
  - ideas: List[str]

## Notes
- Requires valid Serper and OpenAI API keys.
- All tasks are executed sequentially.
- Project ideas are tailored using a custom tool.

## License
MIT 