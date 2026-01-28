# ================================
# Utility Functions & Test Helpers
# ================================

import requests
import json
from typing import Optional
from datetime import datetime

BASE_URL = "http://localhost:8000"


# ================================
# Pretty Print Helper
# ================================

def print_html(content: str, title: str = "Output"):
    """Print formatted output (simulates HTML display in notebooks)."""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)
    print(content)
    print('='*50 + "\n")


# ================================
# Test Helper Functions
# ================================

def test_send_email(
    recipient: str = "test@example.com",
    subject: str = "Test Email",
    body: str = "This is a test email."
) -> dict:
    """Send a test email and return the response."""
    payload = {
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "sender": "you@email.com"
    }
    response = requests.post(f"{BASE_URL}/send", json=payload)
    result = response.json()
    print_html(json.dumps(result, indent=2), "Send Email Result")
    return result


def test_get_email(email_id: int) -> dict:
    """Fetch a specific email by ID."""
    response = requests.get(f"{BASE_URL}/emails/{email_id}")
    result = response.json()
    print_html(json.dumps(result, indent=2, default=str), f"Email ID: {email_id}")
    return result


def test_list_emails() -> list:
    """List all emails."""
    response = requests.get(f"{BASE_URL}/emails")
    result = response.json()
    print_html(json.dumps(result, indent=2, default=str), "All Emails")
    return result


def test_unread_emails() -> list:
    """List unread emails."""
    response = requests.get(f"{BASE_URL}/emails/unread")
    result = response.json()
    print_html(json.dumps(result, indent=2, default=str), "Unread Emails")
    return result


def test_search_emails(query: str) -> list:
    """Search emails by keyword."""
    response = requests.get(f"{BASE_URL}/emails/search", params={"q": query})
    result = response.json()
    print_html(json.dumps(result, indent=2, default=str), f"Search Results: '{query}'")
    return result


def test_filter_emails(
    recipient: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> list:
    """Filter emails by recipient and/or date range."""
    params = {}
    if recipient:
        params["recipient"] = recipient
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    response = requests.get(f"{BASE_URL}/emails/filter", params=params)
    result = response.json()
    print_html(json.dumps(result, indent=2, default=str), "Filtered Emails")
    return result


def test_mark_read(email_id: int) -> dict:
    """Mark an email as read."""
    response = requests.patch(f"{BASE_URL}/emails/{email_id}/read")
    result = response.json()
    print_html(json.dumps(result, indent=2), f"Mark Read: Email {email_id}")
    return result


def test_mark_unread(email_id: int) -> dict:
    """Mark an email as unread."""
    response = requests.patch(f"{BASE_URL}/emails/{email_id}/unread")
    result = response.json()
    print_html(json.dumps(result, indent=2), f"Mark Unread: Email {email_id}")
    return result


def test_delete_email(email_id: int) -> dict:
    """Delete an email by ID."""
    response = requests.delete(f"{BASE_URL}/emails/{email_id}")
    result = response.json()
    print_html(json.dumps(result, indent=2), f"Delete Email: {email_id}")
    return result


def reset_database() -> dict:
    """Reset the email database to initial state."""
    response = requests.get(f"{BASE_URL}/reset_database")
    result = response.json()
    print_html(json.dumps(result, indent=2), "Database Reset")
    return result
