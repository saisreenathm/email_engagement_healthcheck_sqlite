# test_fetch_and_store.py

from gmail_auth import authenticate_gmail
from gmail_fetcher import get_promotional_threads
from db import init_db, get_emails_by_filter

def run_test():
    print("🔧 Initializing DB...")
    init_db()

    print("🔐 Authenticating Gmail...")
    service = authenticate_gmail()
    if service is None:
        print("❌ Gmail auth failed.")
        return

    print("📥 Fetching threads...")
    threads = get_promotional_threads(service, max_threads=3)
    print(f"✅ {len(threads)} threads fetched and stored.")

    print("🔍 Checking DB contents...")
    emails = get_emails_by_filter()
    for email in emails:
        print(f"[{email['timestamp']}] From: {email['sender']} | Subj: {email['subject']}")

if __name__ == "__main__":
    run_test()
