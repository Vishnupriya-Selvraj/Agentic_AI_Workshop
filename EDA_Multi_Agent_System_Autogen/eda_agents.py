import autogen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Configuration for the agents - adjust as needed
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo", "gemini-1.5-flash-latest"], # Add gemini-1.5-flash-latest
    },
)

# 1. Admin Agent
admin_agent = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Oversees the workflow, ensures coordination, and maintains alignment with project goals.",
    code_execution_config=False, # Admin doesn't execute code directly
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="ALWAYS",
)

# 2. Data Preparation Agent
data_prep_agent = autogen.AssistantAgent(
    name="Data_Preparation_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Data Preparation Agent. You handle data cleaning, preprocessing, and feature engineering."
        "Your tasks include handling missing values, encoding categorical variables, scaling numerical features, etc."
        "Once done, you will pass the cleaned data (e.g., as a pandas DataFrame) to the EDA Agent."
    ),
)

# 3. EDA Agent
eda_agent = autogen.AssistantAgent(
    name="EDA_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are an EDA Agent. You perform statistical summarization, generate insights, and create visualizations."
        "You will receive cleaned data from the Data Preparation Agent."
        "Once your analysis and visualizations are ready, you will pass the insights and visualization code to the Report Generator Agent."
    ),
)

# 4. Report Generator Agent
report_generator_agent = autogen.AssistantAgent(
    name="Report_Generator_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Report Generator Agent. Your role is to create a well-structured EDA report."
        "You will receive insights and visualization code from the EDA Agent."
        "Your report should include an overview of the data, key insights, detailed visualizations, and conclusions."
        "You should be ready to incorporate feedback from the Critic Agent."
    ),
)

# 5. Critic Agent
critic_agent = autogen.AssistantAgent(
    name="Critic_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Critic Agent. You review the outputs from other agents, especially the Report Generator."
        "Provide constructive feedback to improve clarity, accuracy, and actionability of the EDA report and insights."
        "If the report is satisfactory, approve it. Otherwise, request revisions."
    ),
)

# 6. Executor Agent
executor_agent = autogen.UserProxyAgent(
    name="Executor",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "./scratchpad", # Directory for code execution
        "use_docker": False, # Set to True if Docker is available and preferred
    },
    system_message="Executor agent. Validates code and ensures the accuracy of results."
)

# Create a group chat for the agents
groupchat = autogen.GroupChat(
    agents=[admin_agent, data_prep_agent, eda_agent, report_generator_agent, critic_agent, executor_agent],
    messages=[],
    max_round=20, # Increased max rounds for complex tasks
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

def run_eda_workflow(data_path: str):
    """Runs the EDA multi-agent workflow with a given dataset."""
    # Initial prompt for the Admin agent to kick off the workflow
    admin_agent.initiate_chat(
        manager,
        message=f"Perform a comprehensive EDA on the dataset located at {data_path}. "
                "The workflow should involve data preparation, EDA, report generation, and critic review."
                "Ensure the final report is well-structured and includes visualizations."
    )

if __name__ == "__main__":
    # Example Usage:
    # For demonstration, let's create a dummy CSV file
    dummy_data = {
        'Feature1': np.random.rand(100),
        'Feature2': np.random.randint(1, 10, 100),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'Target': np.random.rand(100) * 100
    }
    dummy_df = pd.DataFrame(dummy_data)
    dummy_csv_path = "dummy_dataset.csv"
    dummy_df.to_csv(dummy_csv_path, index=False)

    print(f"Created dummy dataset at: {dummy_csv_path}")
    
    # Run the EDA workflow with the dummy dataset
    run_eda_workflow(dummy_csv_path) 