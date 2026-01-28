# ================================
# Display Functions for Agent Output
# ================================
"""
Pretty printing utilities for chat completions and tool calls.
"""

import json
from typing import Any


def pretty_print_chat_completion(response: Any) -> None:
    """
    Pretty print a chat completion response, including tool calls.

    Args:
        response: The response object from client.chat.completions.create()
    """
    print("\n" + "="*60)
    print("  AGENT RESPONSE")
    print("="*60)

    # Handle different response structures
    if hasattr(response, 'choices') and response.choices:
        for i, choice in enumerate(response.choices):
            message = choice.message

            # Print role
            role = getattr(message, 'role', 'assistant')
            print(f"\n[{role.upper()}]")

            # Print content if available
            content = getattr(message, 'content', None)
            if content:
                print(f"\n{content}")

            # Print tool calls if available
            tool_calls = getattr(message, 'tool_calls', None)
            if tool_calls:
                print("\n" + "-"*40)
                print("  TOOL CALLS")
                print("-"*40)
                for tc in tool_calls:
                    print(f"\n  Tool: {tc.function.name}")
                    try:
                        args = json.loads(tc.function.arguments)
                        print(f"  Args: {json.dumps(args, indent=2)}")
                    except:
                        print(f"  Args: {tc.function.arguments}")

    # Handle AISuite specific response format
    elif hasattr(response, 'message'):
        message = response.message
        if hasattr(message, 'content') and message.content:
            print(f"\n{message.content}")

    # Handle dict response
    elif isinstance(response, dict):
        if 'choices' in response:
            for choice in response['choices']:
                msg = choice.get('message', {})
                if msg.get('content'):
                    print(f"\n{msg['content']}")
                if msg.get('tool_calls'):
                    print("\n" + "-"*40)
                    print("  TOOL CALLS")
                    print("-"*40)
                    for tc in msg['tool_calls']:
                        print(f"\n  Tool: {tc['function']['name']}")
                        print(f"  Args: {tc['function']['arguments']}")
        else:
            print(json.dumps(response, indent=2, default=str))

    # Fallback: try to print as JSON
    else:
        try:
            print(json.dumps(response, indent=2, default=str))
        except:
            print(response)

    print("\n" + "="*60 + "\n")


def print_tool_trace(tool_name: str, args: dict, result: Any) -> None:
    """
    Print a trace of a tool execution.

    Args:
        tool_name: Name of the tool that was called.
        args: Arguments passed to the tool.
        result: Result returned by the tool.
    """
    print(f"\n>>> Tool: {tool_name}")
    print(f"    Args: {json.dumps(args, indent=2)}")
    print(f"    Result: {json.dumps(result, indent=2, default=str)[:500]}...")


def print_email_summary(emails: list) -> None:
    """
    Print a summary table of emails.

    Args:
        emails: List of email dictionaries.
    """
    if not emails:
        print("\n  No emails found.\n")
        return

    print("\n" + "-"*70)
    print(f"  {'ID':<5} {'From':<25} {'Subject':<30} {'Read':<5}")
    print("-"*70)

    for email in emails:
        email_id = email.get('id', 'N/A')
        sender = email.get('sender', 'Unknown')[:23]
        subject = email.get('subject', 'No Subject')[:28]
        read = "Yes" if email.get('read', False) else "No"
        print(f"  {email_id:<5} {sender:<25} {subject:<30} {read:<5}")

    print("-"*70 + "\n")
