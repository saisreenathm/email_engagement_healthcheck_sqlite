# test_analyzer.py

from analyzer import analyze_conversations

def run():
    print("🔍 Running Gemini AI analysis on email threads...")
    results = analyze_conversations()

    for res in results:
        print(f"\n🧵 Thread ID: {res['thread_id']}")
        print(f"   📧 Messages: {res['num_messages']}")
        print(f"   📊 Engagement Score: {res['engagement_score']}")
        print(f"   😊 Sentiment: {res['sentiment']}")
        print(f"   ⏱️ Responsiveness: {res.get('responsiveness', 'N/A')}")
        print(f"   🤝 Relationship Quality: {res.get('relationship_quality', 'N/A')}")
        print(f"   ⚠️ Risk Alerts: {', '.join(res['risk_alerts']) or 'None'}")

if __name__ == "__main__":
    run()
