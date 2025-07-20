import autogen

# Configuration for the agents
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gemini-1.5-flash-latest"], # Using only gemini-1.5-flash-latest
    },
)

# BMI Calculation Tool
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """Calculates the Body Mass Index (BMI) given weight in kg and height in cm.
    Returns the BMI score and category.
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    category = ""
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    return f"BMI: {bmi:.2f}, Category: {category}"


# 1. User Proxy Agent
user_proxy_agent = autogen.UserProxyAgent(
    name="User_Proxy_Agent",
    system_message=(
        "You are a User Proxy Agent. You collect data from the user and share it with other agents."
        "Collect the following inputs: Weight (kg), Height (cm), Age, Gender, and Dietary Preference (Veg, Non-Veg, Vegan)."
        "Once all information is collected, pass it to the BMI Agent."
        "You also act as the human in the loop for code execution."
    ),
    code_execution_config={
        "work_dir": "./scratchpad",
        "use_docker": False,
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# 2. BMI Agent
bmi_agent = autogen.AssistantAgent(
    name="BMI_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a BMI Agent. You analyze the BMI score to provide health recommendations."
        "You are responsible for calling the 'calculate_bmi' tool."
        "Once BMI is calculated and recommendations are generated, pass the BMI insights and initial health recommendations to the Diet Planner Agent."
    ),
)

# Register the BMI tool with the BMI Agent
bmi_agent.register_for_execution(calculate_bmi)


# 3. Diet Planner Agent
diet_planner_agent = autogen.AssistantAgent(
    name="Diet_Planner_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Diet Planner Agent. You provide meal suggestions based on BMI insights and dietary preferences."
        "Receive BMI insights from the BMI Agent and dietary preferences from the User Proxy Agent."
        "Once a tailored meal plan is created, relay it to the Workout Scheduler Agent."
    ),
)

# 4. Workout Scheduler Agent
workout_scheduler_agent = autogen.AssistantAgent(
    name="Workout_Scheduler_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Workout Scheduler Agent. You create tailored weekly workout plans."
        "Receive meal plan suggestions from the Diet Planner Agent and user's age and gender from the User Proxy Agent."
        "Provide a comprehensive weekly workout plan and conclude the conversation with 'TERMINATE'."
    ),
)

# Define the sequential conversation flow
def run_health_assistant_workflow():
    # The User Proxy Agent initiates the conversation by collecting data
    user_input_message = (
        "Hello! I need a health plan. Please provide me with your Weight (kg), Height (cm), Age, Gender, and Dietary Preference (Veg, Non-Veg, Vegan)."
    )

    # Initiate conversation from User Proxy Agent to BMI Agent
    # The conversation will flow sequentially as defined by the agents' system messages
    user_proxy_agent.initiate_chat(
        bmi_agent,
        message=user_input_message,
        max_turns=10, # Allow enough turns for sequential flow
    )

if __name__ == "__main__":
    print("Starting Smart Health Assistant...")
    run_health_assistant_workflow() 