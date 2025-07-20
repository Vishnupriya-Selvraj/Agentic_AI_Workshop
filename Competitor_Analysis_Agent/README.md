# Competitor Analysis Agent

This project implements a conversational AI pipeline to analyze nearby clothing store competitors. It provides insights into footfall trends and peak hours, helping businesses optimize their strategies.

## Setup

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd Competitor_Analysis_Agent
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

3. Set your API keys:

   Open `main.py` and replace `"YOUR_OPENAI_API_KEY"` and `"YOUR_TAVILY_API_KEY"` with your actual OpenAI and Tavily API keys, respectively.

   ```python
   os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
   os.environ["TAVILY_API_KEY"] = "YOUR_TAVILY_API_KEY"
   ```

## Usage

Run the `main.py` script to start the conversational agent:

```bash
python main.py
```

Then, you can interact with the agent in your terminal to get reports on clothing store competitors. 