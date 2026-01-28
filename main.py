# ================================
# Email Assistant Agent - Main
# ================================

# --- Third-party ---
from dotenv import load_dotenv
import aisuite as ai
import json

# --- Local / project ---
import utils
import display_functions
import email_tools


# ================================
# Environment & Client
# ================================
import os
from pathlib import Path

# Load environment variables from .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

client = ai.Client()   # Initialize AISuite client


# ================================
# Prompt Builder
# ================================

def build_prompt(request_: str) -> str:
    """
    Wrap a user request with system instructions for the email assistant.

    Args:
        request_: The natural language request from the user.

    Returns:
        A formatted prompt with system instructions.
    """
    return f"""
- You are an AI assistant specialized in managing emails.
- You can perform various actions such as listing, searching, filtering, and manipulating emails.
- Use the provided tools to interact with the email system.
- Never ask the user for confirmation before performing an action.
- If needed, my email address is "you@email.com" so you can use it to send emails or perform actions related to my account.

{request_.strip()}
"""


# ================================
# Example Usage
# ================================

if __name__ == "__main__":
    # Example: Print the formatted prompt
    example_prompt = build_prompt("Delete the Happy Hour email")
    utils.print_html(content=example_prompt, title="Example Prompt")

    # ================================
    # Test the email tools (uncomment to try)
    # ================================

    # Test sending a new email and fetch it by ID
    # new_email = email_tools.send_email("test@example.com", "Lunch plans", "Shall we meet at noon?")
    # content_ = email_tools.get_email(new_email['id'])

    # Uncomment the ones you want to try:
    # content_ = email_tools.list_all_emails()
    # content_ = email_tools.list_unread_emails()
    # content_ = email_tools.search_emails("lunch")
    # content_ = email_tools.filter_emails(recipient="test@example.com")
    # content_ = email_tools.mark_email_as_read(new_email['id'])
    # content_ = email_tools.mark_email_as_unread(new_email['id'])
    # content_ = email_tools.search_unread_from_sender("test@example.com")
    # content_ = email_tools.delete_email(new_email['id'])

    # utils.print_html(content=json.dumps(content_, indent=2), title="Testing the email_tools")

    # ================================
    # LLM + Email Tools Examples
    # ================================

    # Example 1: Check unread emails from boss and send follow-up
    # prompt_ = build_prompt("Check for unread emails from boss@email.com, mark them as read, and send a polite follow-up.")
    #
    # response = client.chat.completions.create(
    #     model="anthropic:claude-sonnet-4-20250514",
    #     messages=[{"role": "user", "content": prompt_}],
    #     tools=[
    #         email_tools.search_unread_from_sender,
    #         email_tools.list_unread_emails,
    #         email_tools.search_emails,
    #         email_tools.get_email,
    #         email_tools.mark_email_as_read,
    #         email_tools.send_email
    #     ],
    #     max_turns=5,
    # )
    # display_functions.pretty_print_chat_completion(response)

    # Example 2: Delete Happy Hour email (with delete_email tool)
    # prompt_ = build_prompt("Delete the happy hour email")
    #
    # response = client.chat.completions.create(
    #     model="anthropic:claude-sonnet-4-20250514",
    #     messages=[{"role": "user", "content": prompt_}],
    #     tools=[
    #         email_tools.search_unread_from_sender,
    #         email_tools.list_unread_emails,
    #         email_tools.search_emails,
    #         email_tools.get_email,
    #         email_tools.mark_email_as_read,
    #         email_tools.send_email,
    #         email_tools.delete_email
    #     ],
    #     max_turns=5
    # )
    # display_functions.pretty_print_chat_completion(response)

    print("\n[INFO] Email Assistant Agent ready.")
    print("[INFO] Start the email service first: python email_service.py")
    print("[INFO] Then uncomment examples above to test the agent.\n")
