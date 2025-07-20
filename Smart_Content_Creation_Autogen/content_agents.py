import autogen

# Configuration for the agents
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo", "gemini-1.5-flash-latest"], # Adjust models as per your OAI_CONFIG_LIST
    },
)

# 1. Content Creator Agent
content_creator_agent = autogen.AssistantAgent(
    name="Content_Creator",
    llm_config={"config_list": config_list},
    system_message=(
        "You are the Content Creator Agent. Your role is to draft content on topics involving Generative AI."
        "Ensure the content is clear, concise, and technically accurate."
        "You will receive feedback from the Content Critic Agent and revise your content iteratively (max 5 turns)."
        "When you are done, output FINAL CONTENT: followed by the markdown of the content."
    ),
)

# 2. Content Critic Agent
content_critic_agent = autogen.AssistantAgent(
    name="Content_Critic",
    llm_config={"config_list": config_list},
    system_message=(
        "You are the Content Critic Agent. Your role is to evaluate the content drafted by the Content Creator Agent."
        "Provide feedback on language and technical correctness, and suggest improvements."
        "You will provide feedback for a maximum of 5 turns of revision."
        "If the content is satisfactory, reply with 'Looks good! TERMINATE'. Otherwise, provide detailed feedback for revision."
    ),
)

# Create a group chat for the agents (optional, but good for structured conversation)
# For a two-agent conversation, we can directly initiate chat between them.

# Simulate the conversation
if __name__ == "__main__":
    # Topic for discussion
    topic = "Agentic AI"

    # Initial content drafting by Content Creator
    initial_prompt = f"Draft an initial piece of content (around 200 words) on the topic: {topic}"

    # Initiate the chat between Content Creator and Content Critic
    # The Content Creator will initiate, and the Critic will provide feedback.
    # The conversation will run for a maximum of 5 turns.
    chat_result = content_critic_agent.initiate_chat(
        content_creator_agent,
        message=initial_prompt,
        max_turns=5,
    )

    # Display the final content by searching for the last message from the Content_Creator that starts with "FINAL CONTENT:"
    final_content = "No final content generated."
    # Iterate through chat history in reverse to find the last FINAL CONTENT message
    for entry in reversed(chat_result.chat_history):
        # Autogen's chat_history can have different structures. Try to be robust.
        messages_in_entry = []
        if isinstance(entry, dict) and "messages" in entry:
            messages_in_entry = entry["messages"]
        elif isinstance(entry, dict) and "content" in entry and "sender" in entry:
            messages_in_entry = [entry] # It's a single message dict
        elif isinstance(entry, str):
            # If it's just a string, it might be a direct message from an agent
            # This case is less likely to contain structured FINAL CONTENT, but we'll check
            if entry.startswith(content_creator_agent.name + ":") and "FINAL CONTENT:" in entry:
                # Attempt to parse if it's a direct agent message with the marker
                content_part = entry.split("FINAL CONTENT:", 1)[1].strip()
                if content_part.startswith("```") and content_part.endswith("```"):
                    lines = content_part.split('\n')
                    if len(lines) > 2:
                        final_content = "\n".join(lines[1:-1]).strip()
                    else:
                        final_content = content_part
                else:
                    final_content = content_part
                break # Found it, break outer loop

        for msg in reversed(messages_in_entry):
            if isinstance(msg, dict) and msg.get("sender") == content_creator_agent.name and isinstance(msg.get("content"), str):
                content = msg["content"]
                # Check for FINAL CONTENT: marker
                if content.startswith("FINAL CONTENT:"):
                    # Extract content after the marker
                    extracted_text = content.replace("FINAL CONTENT:", "").strip()
                    # If it's a markdown code block, extract from there
                    if extracted_text.startswith("```") and extracted_text.endswith("```"):
                        # Remove the markdown code block fences and language specifier (e.g., ```markdown)
                        lines = extracted_text.split('\n')
                        if len(lines) > 2:
                            final_content = "\n".join(lines[1:-1]).strip()
                        else:
                            final_content = extracted_text # Fallback if empty block or single line
                    else:
                        final_content = extracted_text
                    break # Found the last FINAL CONTENT, exit inner loop
        if final_content != "No final content generated.":
            break # Found the last FINAL CONTENT, exit outer loop

    print("\n\n### Final Refined Content ###")
    print(final_content) 