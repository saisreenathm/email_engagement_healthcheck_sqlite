# main.py

import streamlit as st
import pandas as pd
from analyzer import analyze_conversations
from db import init_db, get_emails_by_filter

st.set_page_config(page_title="Email Engagement Health Check", layout="wide")

def main():
    st.title("📬 Email Engagement Health Check")
    st.write("Analyze email threads from your database using Gemini AI.")

    init_db()  # Ensure the database schema exists

    with st.sidebar:
        st.header("🔍 Filter Emails")
        sender_filter = st.text_input("Sender Email (optional)")
        start_date = st.date_input("Start Date (optional)", format="YYYY-MM-DD")
        end_date = st.date_input("End Date (optional)", format="YYYY-MM-DD")
        run = st.button("Run Analysis")

    if run:
        run_analysis(sender_filter, start_date, end_date)

def run_analysis(sender_filter, start_date, end_date):
    with st.spinner("🔎 Analyzing conversations..."):
        # Convert date input to ISO string if present
        start_str = start_date.isoformat() if start_date else None
        end_str = end_date.isoformat() if end_date else None

        results = analyze_conversations(
            sender=sender_filter or None,
            start_date=start_str,
            end_date=end_str
        )

        if not results:
            st.warning("No conversations found for the given filters.")
            return

        # Prepare and show summary table
        summary_data = []
        for res in results:
            summary_data.append({
                "Thread ID": res["thread_id"],
                "Messages": res["num_messages"],
                "Engagement": res["engagement_score"],
                "Sentiment": res["sentiment"],
                "Responsiveness": res.get("responsiveness", "N/A"),
                "Relationship Summary": res.get("relationship_quality", "N/A"),
                "Risk Analysis": ", ".join(res.get("risk_alerts", [])) or "None"
            })

        st.markdown("### 📊 Gemini AI Thread Analysis Summary")
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

        # Show each thread's conversation in expandable view
        st.markdown("### 🧵 Email Thread Details")
        all_emails = get_emails_by_filter(sender=sender_filter or None, start_date=start_str, end_date=end_str)

        for res in results:
            thread_id = res["thread_id"]
            with st.expander(f"📨 View Thread {thread_id}", expanded=False):
                thread_emails = [e for e in all_emails if e["thread_id"] == thread_id]
                email_data = []
                for email in thread_emails:
                    email_data.append({
                        "From": email['sender'],
                        "To": email['recipient'],
                        "Subject": email['subject'],
                        "Timestamp": email['timestamp'],
                        "Body": email['body'][:120] + "..." if len(email['body']) > 120 else email['body']
                    })
                st.dataframe(pd.DataFrame(email_data), use_container_width=True)

if __name__ == "__main__":
    main()
