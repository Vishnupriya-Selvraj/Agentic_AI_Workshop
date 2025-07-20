import autogen
from PIL import Image
import io

# Configuration for the agents
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gemini-1.5-flash-latest"], # Using only gemini-1.5-flash-latest
    },
)

# Placeholder for image processing (OCR simulation)
def process_bill_image_dummy(image_path: str) -> dict:
    """Simulates processing a bill image and extracting expenses.
    In a real application, this would involve OCR and intelligent parsing.
    For demonstration, it returns a predefined set of categorized expenses.
    """
    print(f"\nProcessing dummy bill image from: {image_path}")
    # Simulate extracting data from a bill
    dummy_expenses = {
        "Groceries": 55.75,
        "Dining": 30.50,
        "Utilities": 75.00,
        "Shopping": 120.00,
        "Entertainment": 45.25,
    }
    total_amount = sum(dummy_expenses.values())
    return {"categorized_expenses": dummy_expenses, "total_amount": total_amount}

# 1. User Proxy Agent
user_proxy_agent = autogen.UserProxyAgent(
    name="User_Proxy_Agent",
    system_message=(
        "You are a User Proxy Agent. You initiate the chat with the Group Manager."
        "Your role is to provide the path to a bill image that needs to be processed."
        "You also act as the human in the loop for code execution."
    ),
    code_execution_config={
        "work_dir": "./scratchpad",
        "use_docker": False,
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# 2. Bill Processing Agent
bill_processing_agent = autogen.AssistantAgent(
    name="Bill_Processing_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are a Bill Processing Agent. You extract data from uploaded bill images and organize expenses into categories."
        "You will receive an image path from the Group Manager. Call the 'process_bill_image_dummy' tool to simulate extraction."
        "Your output should be a categorized list of all expenses with the total amount spent. Pass this to the Expense Summarization Agent."
    ),
)

# Register the dummy bill processing tool with the Bill Processing Agent
bill_processing_agent.register_for_execution(process_bill_image_dummy)

# 3. Expense Summarization Agent
expense_summarization_agent = autogen.AssistantAgent(
    name="Expense_Summarization_Agent",
    llm_config={"config_list": config_list},
    system_message=(
        "You are an Expense Summarization Agent. You analyze extracted expenses and provide a breakdown of total spending per category."
        "You will receive a categorized list of expenses from the Bill Processing Agent."
        "Highlight any unusual or high spending trends. Your final output should be a summary of spending trends, showing which category has the highest expenditure. Conclude with 'TERMINATE'."
    ),
)

# Define the Group Chat and Manager
groupchat = autogen.GroupChat(
    agents=[
        user_proxy_agent,
        bill_processing_agent,
        expense_summarization_agent,
    ],
    messages=[],
    max_round=8, # Increased max rounds for sequential tasks
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

def run_bill_management_workflow(image_path: str):
    initial_message = f"Please process the bill image located at: {image_path}"
    user_proxy_agent.initiate_chat(manager, message=initial_message)

if __name__ == "__main__":
    print("Starting Bill Managing Agent...")
    dummy_image_path = "dummy_bill.png"
    # Create a dummy image file (a blank PNG for simulation)
    try:
        Image.new('RGB', (100, 50), color = 'red').save(dummy_image_path)
        print(f"Created dummy image file: {dummy_image_path}")
    except Exception as e:
        print(f"Could not create dummy image: {e}. Please ensure Pillow is installed.")

    run_bill_management_workflow(dummy_image_path) 