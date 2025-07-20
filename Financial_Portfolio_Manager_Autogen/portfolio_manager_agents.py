import autogen

# Configuration for the agents
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gemini-1.5-flash-latest"], # Using only gemini-1.5-flash-latest
    },
)

# 1. User Proxy Agent
user_proxy_agent = autogen.UserProxyAgent(
    name="User_Proxy_Agent",
    system_message=(
        "You are a User Proxy Agent. You initiate the chat with the Group Chat Manager."
        "Inform the Group Chat Manager about the user's intention to manage their investments."
        "You also act as the human in the loop for code execution if needed."
    ),
    code_execution_config={
        "work_dir": "./scratchpad",
        "use_docker": False,
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# 2. Portfolio Analysis Agent
portfolio_analysis_agent = autogen.AssistantAgent(
    name="Portfolio_Analysis_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Portfolio Analysis Agent. You summarize the user's existing investment portfolio and determine the investment category (Growth or Value)."
        "Ask the user for their current salary and a summary of their current investment portfolio (e.g., amounts in fixed deposits, SIPs, real estate, etc.)."
        "Based on this information, explicitly state whether to pursue 'Growth' or 'Value' investments."
        "When you are done, pass this information to the Investment Advisor Agent along with the chosen investment category."
    ),
)

# 3. Growth Investment Agent
growth_investment_agent = autogen.AssistantAgent(
    name="Growth_Investment_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Growth Investment Agent. You suggest investments for maximizing portfolio growth."
        "Provide recommendations for high-growth investment options. When you are done, pass your recommendations to the Investment Advisor Agent."
    ),
)

# 4. Value Investment Agent
value_investment_agent = autogen.AssistantAgent(
    name="Value_Investment_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Value Investment Agent. You recommend stable investments for long-term value."
        "Provide recommendations for stable, long-term investment options. When you are done, pass your recommendations to the Investment Advisor Agent."
    ),
)

# 5. Investment Advisor Agent
investment_advisor_agent = autogen.AssistantAgent(
    name="Investment_Advisor_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are an Investment Advisor Agent. You compile a detailed report of holdings and recommendations."
        "Generate a personalized financial report based on the insights from previous agents (Portfolio Analysis, Growth/Value Investment)."
        "The report should include portfolio analysis, growth/value investment suggestions, and a summary. Conclude the report with 'TERMINATE'."
    ),
)

# Define the Group Chat and Manager
groupchat = autogen.GroupChat(
    agents=[
        user_proxy_agent,
        portfolio_analysis_agent,
        growth_investment_agent,
        value_investment_agent,
        investment_advisor_agent,
    ],
    messages=[],
    max_round=15, # Increased max rounds for complex tasks
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

# StateFlow for dynamic workflow management (simulated within the manager's role)
# The manager will dynamically call agents based on conversation content

def run_portfolio_manager_workflow():
    initial_message = "I want to manage my investments and get a personalized financial report."
    user_proxy_agent.initiate_chat(manager, message=initial_message)

if __name__ == "__main__":
    print("Starting Financial Portfolio Manager...")
    run_portfolio_manager_workflow() 