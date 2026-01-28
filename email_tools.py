# ================================
# Email Tools for LLM Agent
# ================================
"""
These tools wrap the email service REST API endpoints,
making them available for the LLM to call as functions.
"""

import requests
import json
from typing import Optional, List

BASE_URL = "http://localhost:8000"


# ================================
# Tool Functions
# ================================

def list_all_emails() -> list:
    """Fetch all emails from the inbox, ordered by newest first."""
    response = requests.get(f"{BASE_URL}/emails")
    return response.json()


def list_unread_emails() -> list:
    """Retrieve only unread emails from the inbox."""
    response = requests.get(f"{BASE_URL}/emails/unread")
    return response.json()


def search_emails(query: str) -> list:
    """
    Search emails by keyword in subject, body, or sender.

    Args:
        query: The search term to look for in emails.

    Returns:
        List of matching emails.
    """
    response = requests.get(f"{BASE_URL}/emails/search", params={"q": query})
    return response.json()


def filter_emails(
    recipient: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> list:
    """
    Filter emails by recipient and/or date range.

    Args:
        recipient: Filter by recipient email address.
        start_date: Filter emails after this date (ISO format).
        end_date: Filter emails before this date (ISO format).

    Returns:
        List of filtered emails.
    """
    params = {}
    if recipient:
        params["recipient"] = recipient
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    response = requests.get(f"{BASE_URL}/emails/filter", params=params)
    return response.json()


def get_email(email_id: int) -> dict:
    """
    Fetch a specific email by its ID.

    Args:
        email_id: The unique identifier of the email.

    Returns:
        The email details as a dictionary.
    """
    response = requests.get(f"{BASE_URL}/emails/{email_id}")
    return response.json()


def mark_email_as_read(email_id: int) -> dict:
    """
    Mark an email as read.

    Args:
        email_id: The unique identifier of the email to mark as read.

    Returns:
        Confirmation message.
    """
    response = requests.patch(f"{BASE_URL}/emails/{email_id}/read")
    return response.json()


def mark_email_as_unread(email_id: int) -> dict:
    """
    Mark an email as unread.

    Args:
        email_id: The unique identifier of the email to mark as unread.

    Returns:
        Confirmation message.
    """
    response = requests.patch(f"{BASE_URL}/emails/{email_id}/unread")
    return response.json()


def send_email(recipient: str, subject: str, body: str) -> dict:
    """
    Send a new email.

    Args:
        recipient: The email address of the recipient.
        subject: The subject line of the email.
        body: The body content of the email.

    Returns:
        Confirmation with the new email's ID.
    """
    payload = {
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "sender": "you@email.com"
    }
    response = requests.post(f"{BASE_URL}/send", json=payload)
    return response.json()


def delete_email(email_id: int) -> dict:
    """
    Delete an email by its ID.

    Args:
        email_id: The unique identifier of the email to delete.

    Returns:
        Confirmation message.
    """
    response = requests.delete(f"{BASE_URL}/emails/{email_id}")
    return response.json()


def search_unread_from_sender(sender_address: str) -> list:
    """
    Return unread emails from a specific sender.

    Args:
        sender_address: The email address of the sender (e.g., boss@email.com).

    Returns:
        List of unread emails from the specified sender.
    """
    # Get all unread emails
    unread = requests.get(f"{BASE_URL}/emails/unread").json()

    # Filter by sender
    return [email for email in unread if email.get("sender", "").lower() == sender_address.lower()]
