# Automated Code Debugging Assistant (CrewAI)

## Overview
A CrewAI-powered system that analyzes and corrects errors in Python code using a sequential, planning-enabled workflow. The system consists of three agents: Code Analyzer, Code Corrector, and Manager.

## Features
- **Code Analyzer Agent:** Identifies syntax and logical errors in Python code using a custom CodeInterpreterTool.
- **Code Corrector Agent:** Fixes the identified errors and returns the corrected code.
- **Manager Agent:** Oversees the process and ensures smooth task execution.
- **Planning Enabled:** Agents can plan and coordinate steps for effective debugging.

## Setup
1. **Clone the repository and navigate to the project directory:**
   ```sh
   git clone <your-repo-url>
   cd Automated_Code_Debugging_Assistant
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
4. **Create a `.env` file in the project root if using OpenAI, Groq, or Gemini APIs:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   # or
   GROQ_API_KEY=your_groq_api_key_here
   # or
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage
Run the main script:
```sh
python debugging_crew.py
```
You can modify the input code in the `__main__` section.

## Output Structure
- **Code Analyzer Output:** List of errors (e.g., indentation issues, logical errors).
- **Code Corrector Output:** The corrected version of the Python code.

## Notes
- Requires a valid API key for LLM-based agents if you want to use OpenAI, Groq, or Gemini.
- All tasks are executed sequentially with planning enabled.

## License
MIT 