# test_seed_data.py

from db import insert_email
from datetime import datetime, timedelta
import random

now = datetime.now()

def generate_timestamp(days_ago: int, hours_offset: int = 0):
    dt = now - timedelta(days=days_ago, hours=hours_offset)
    return str(int(dt.timestamp() * 1000))  # Gmail uses milliseconds

def seed_emails():
    threads = [
        {
            "thread_id": "thread_1",
            "emails": [
                {
                    "sender": "client@example.com",
                    "recipient": "support@softco.com",
                    "subject": "App not syncing with cloud",
                    "body": "Hi, I'm having issues with cloud sync. It's really frustrating. Please help.",
                    "timestamp": generate_timestamp(5, 10)
                },
                {
                    "sender": "support@softco.com",
                    "recipient": "client@example.com",
                    "subject": "RE: App not syncing with cloud",
                    "body": "We're sorry to hear that. Can you provide your account ID so we can assist?",
                    "timestamp": generate_timestamp(5, 6)
                },
                {
                    "sender": "client@example.com",
                    "recipient": "support@softco.com",
                    "subject": "RE: App not syncing with cloud",
                    "body": "Still no response. Very disappointed.",
                    "timestamp": generate_timestamp(3)
                }
            ]
        },
        {
            "thread_id": "thread_2",
            "emails": [
                {
                    "sender": "client@example.com",
                    "recipient": "sales@softco.com",
                    "subject": "Interested in your enterprise plan",
                    "body": "Hey team, we’re exploring your software for our startup. Can you send a demo link?",
                    "timestamp": generate_timestamp(7)
                },
                {
                    "sender": "sales@softco.com",
                    "recipient": "client@example.com",
                    "subject": "RE: Interested in your enterprise plan",
                    "body": "Sure! Here's the demo link and pricing details. Let us know if you'd like a call.",
                    "timestamp": generate_timestamp(6, 20)
                },
                {
                    "sender": "client@example.com",
                    "recipient": "sales@softco.com",
                    "subject": "RE: Interested in your enterprise plan",
                    "body": "Thanks, we’ll review this week.",
                    "timestamp": generate_timestamp(5, 12)
                },
                {
                    "sender": "sales@softco.com",
                    "recipient": "client@example.com",
                    "subject": "RE: Interested in your enterprise plan",
                    "body": "Just following up — would you like to schedule a call?",
                    "timestamp": generate_timestamp(2)
                }
            ]
        },
        {
            "thread_id": "thread_3",
            "emails": [
                {
                    "sender": "client@example.com",
                    "recipient": "help@softco.com",
                    "subject": "Payment issue",
                    "body": "My invoice was double charged. This needs urgent resolution.",
                    "timestamp": generate_timestamp(4)
                }
            ]
        }
    ]

    for thread in threads:
        for email in thread["emails"]:
            insert_email({
                "thread_id": thread["thread_id"],
                **email
            })
    print("✅ Synthetic emails seeded.")

if __name__ == "__main__":
    seed_emails()
