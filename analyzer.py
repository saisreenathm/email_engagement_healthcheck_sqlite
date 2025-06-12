# analyzer.py

import os
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

from db import get_emails_by_filter

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv(
    "GEMINI_API_URL",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
)

def fetch_conversations(sender: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, List[Dict]]:
    emails = get_emails_by_filter(sender=sender, start_date=start_date, end_date=end_date)
    threads = {}
    for email in emails:
        threads.setdefault(email['thread_id'], []).append(email)

    for thread in threads.values():
        thread.sort(key=lambda e: e['timestamp'])
    return threads

def build_gemini_payload(thread: List[Dict]) -> Dict:
    combined_text = "\n".join(
        f"From: {email['sender']}\nSubject: {email['subject']}\nBody: {email['body']}\n"
        for email in thread
    )

    prompt = f"""Analyze the following email thread and provide a JSON object with:
- engagement_score: 'High' (3+ replies), 'Medium' (1-2 replies), or 'Low' (0 replies)
- sentiment: 'Positive', 'Neutral', or 'Negative' based on the tone
- responsiveness: Short summary of how responsive the participants are
- relationship_quality: reply times, last response
- risk_alerts: Eg. 'Customer sounds unhappy' or 'Multiple follow-ups ignored'

Thread:
{combined_text}
Return only the JSON object."""

    return {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

def call_gemini_api(payload: Dict) -> Dict:
    if not GEMINI_API_KEY:
        return {
            "engagement_score": "Unknown",
            "sentiment": "Unknown",
            "responsiveness": "Unknown",
            "relationship_quality": "Unknown",
            "risk_alerts": ["Missing API key"]
        }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        data = response.json()

        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
        if text.strip().startswith("```json"):
            text = text.strip().lstrip("```json").rstrip("```").strip()

        parsed = json.loads(text)

        # 🛠 Fix: ensure risk_alerts is a list
        if isinstance(parsed.get("risk_alerts"), str):
            parsed["risk_alerts"] = [parsed["risk_alerts"]]

        return parsed

    except (requests.RequestException, json.JSONDecodeError) as e:
        return {
            "engagement_score": "Unknown",
            "sentiment": "Unknown",
            "responsiveness": "Unknown",
            "relationship_quality": "Unknown",
            "risk_alerts": [f"Gemini API error: {str(e)}"]
        }

def analyze_conversations(sender: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
    threads = fetch_conversations(sender, start_date, end_date)
    results = []

    for thread_id, emails in threads.items():
        payload = build_gemini_payload(emails)
        result = call_gemini_api(payload)

        results.append({
            "thread_id": thread_id,
            "num_messages": len(emails),
            **result
        })

    return results
