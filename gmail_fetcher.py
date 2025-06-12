# gmail_fetcher.py

import base64
import re
from typing import List, Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from db import insert_email
from gmail_auth import authenticate_gmail

def get_promotional_threads(service, max_threads=5) -> List[Dict]:
    """Fetches up to max_threads promotional email threads."""
    try:
        response = service.users().threads().list(userId='me', labelIds=['CATEGORY_PROMOTIONS'], maxResults=max_threads).execute()
        threads = response.get('threads', [])
        thread_data = []

        for thread in threads:
            thread_id = thread['id']
            thread_response = service.users().threads().get(userId='me', id=thread_id, format='full').execute()
            messages = thread_response.get('messages', [])

            thread_emails = []
            for msg in messages:
                payload = msg.get('payload', {})
                headers = payload.get('headers', [])
                body_data = extract_email_body(msg)

                email = {
                    "thread_id": thread_id,
                    "sender": get_header(headers, 'From'),
                    "recipient": get_header(headers, 'To'),
                    "subject": get_header(headers, 'Subject'),
                    "timestamp": msg.get('internalDate'),
                    "body": body_data
                }

                thread_emails.append(email)
                insert_email(email)  # Store in DB immediately

            thread_data.append({
                "thread_id": thread_id,
                "emails": thread_emails
            })

        return thread_data

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_header(headers, name):
    """Helper to extract a header value."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header.get('value', '')
    return ''

def extract_email_body(message):
    """Extracts text/plain or fallback to text/html as a string."""
    try:
        parts = message.get('payload', {}).get('parts', [])
        if parts:
            for part in parts:
                if part.get('mimeType') == 'text/plain':
                    data = part['body'].get('data')
                    return decode_base64(data)
        # fallback
        data = message.get('payload', {}).get('body', {}).get('data')
        return decode_base64(data)
    except Exception:
        return "[Body not available]"

def decode_base64(data):
    """Decode Gmail-safe base64 to string."""
    if not data:
        return ""
    decoded_bytes = base64.urlsafe_b64decode(data.encode('UTF-8'))
    return decoded_bytes.decode('utf-8', errors='ignore')
