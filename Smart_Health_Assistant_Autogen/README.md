# Smart Health Assistant with Autogen Agents

This project develops a Smart Health Assistant using a sequential multi-agent conversation pattern with Microsoft Autogen. The system collects user data to provide personalized health plans, including BMI insights, tailored meal plans, and workout schedules.

## Objective

To build a Smart Health Assistant that leverages a sequential conversation pattern among specialized agents to deliver comprehensive and personalized health recommendations to the user.

## Key Concepts Used

*   **Sequential Conversation Pattern**: Agents interact in a predefined, linear sequence to achieve a common goal, ensuring a structured flow of information and task execution.
*   **Data Collection**: The `User_Proxy_Agent` is responsible for collecting all necessary user inputs, such as weight, height, age, gender, and dietary preferences.
*   **BMI Calculation**: A `calculate_bmi` tool is implemented and registered to the `BMI_Agent` to compute the user's Body Mass Index.
*   **Health Recommendations**: The `BMI_Agent` analyzes the calculated BMI score and provides suitable health recommendations based on predefined categories (Underweight, Normal weight, Overweight, Obese).
*   **Meal Planning**: The `Diet_Planner_Agent` takes the BMI insights and the user's dietary preferences to suggest a customized meal plan.
*   **Workout Scheduling**: The `Workout_Scheduler_Agent` creates a tailored weekly workout plan, utilizing the meal plan suggestions, user's age, and gender.

## Sequential Conversation Flow

The agents interact in the following sequence:

1.  **User Proxy Agent**
    *   **Role**: Collects all necessary inputs from the user.
    *   **Inputs Expected**: 
        *   Weight (in kg)
        *   Height (in cm)
        *   Age
        *   Gender
        *   Dietary Preference (Veg, Non-Veg, Vegan)

2.  **BMI Tool**
    *   **Role**: Calculates the BMI.
    *   **Formula**: 
        *   Height (in m) = Height (in cm) / 100
        *   BMI = Weight (in kg) / (Height (in m))^2

3.  **BMI Agent**
    *   **Role**: Analyzes the BMI from the tool, determines the BMI category, and provides initial health recommendations.

4.  **Diet Planner Agent**
    *   **Role**: Suggests a tailored meal plan.
    *   **Inputs**: BMI insights from `BMI_Agent` and Dietary preferences from `User_Proxy_Agent`.

5.  **Workout Scheduler Agent**
    *   **Role**: Creates a weekly workout plan.
    *   **Inputs**: Meal plan suggestions from `Diet_Planner_Agent` and Age/Gender from `User_Proxy_Agent`.

## Expected Output

A seamless multi-agent conversation culminating in a complete health plan that includes BMI insights, a tailored diet plan, and a fitness schedule.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd Smart_Health_Assistant_Autogen
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up your LLM configuration. Create an `OAI_CONFIG_LIST` file (JSON format) in the `Smart_Health_Assistant_Autogen` directory. This file should contain a list of dictionaries, where each dictionary specifies an LLM model and its API key. For example, to use Gemini 1.5 Flash:
    ```json
    [
        {
            "model": "gemini-1.5-flash-latest",
            "api_key": "YOUR_GEMINI_API_KEY",
            "api_type": "google",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/"
        }
    ]
    ```
    **Important**: Replace `YOUR_GEMINI_API_KEY` with your actual Google Gemini API key.

## How to Run

To run the Smart Health Assistant system, execute the `health_assistant_agents.py` script:

```bash
python health_assistant_agents.py
```

The script will initiate the conversation with the `User_Proxy_Agent` prompting for user data. Follow the prompts to provide the necessary information, and the agents will proceed sequentially to generate your health plan.

## Future Improvements

*   Integrate with real-time health data sources (wearables, health apps).
*   Allow for more personalized dietary preferences and restrictions.
*   Incorporate a broader range of workout types and intensity levels.
*   Add a feedback loop for users to refine recommendations.
*   Implement persistent storage for user profiles and health history. 