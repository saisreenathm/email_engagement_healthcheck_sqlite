import os
import sqlitecloud
from typing import List, Dict, Optional
from dotenv import load_dotenv
from datetime import datetime

# Load variables from .env
load_dotenv()

SQLITECLOUD_URL = os.getenv("SQLITECLOUD_URL")
if not SQLITECLOUD_URL:
    raise ValueError("Missing SQLITECLOUD_URL in .env file")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id TEXT,
    sender TEXT,
    recipient TEXT,
    subject TEXT,
    timestamp TEXT,
    body TEXT
);
"""

def get_connection():
    """Establish connection to SQLiteCloud."""
    return sqlitecloud.connect(SQLITECLOUD_URL)

def init_db():
    """Initialize the database by creating the required table."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        conn.commit()

def insert_email(email_data: Dict):
    """Insert a single email into the DB, avoiding duplicates."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check for duplicates
        cursor.execute("""
            SELECT 1 FROM emails
            WHERE thread_id = ? AND timestamp = ? AND sender = ?
        """, (email_data['thread_id'], email_data['timestamp'], email_data['sender']))

        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO emails (thread_id, sender, recipient, subject, timestamp, body)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                email_data['thread_id'],
                email_data['sender'],
                email_data['recipient'],
                email_data['subject'],
                email_data['timestamp'],
                email_data['body']
            ))
            conn.commit()

def iso_to_gmail_timestamp(date_str: str) -> str:
    """Convert ISO date (YYYY-MM-DD) to Gmail-style ms timestamp"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return str(int(dt.timestamp() * 1000))  # milliseconds

def get_emails_by_filter(sender: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
    with get_connection() as conn:
        cursor = conn.cursor()

        query = "SELECT * FROM emails WHERE 1=1"
        params = []

        if sender:
            query += " AND sender = ?"
            params.append(sender)

        if start_date:
            query += " AND timestamp >= ?"
            params.append(iso_to_gmail_timestamp(start_date))
        print(end_date, start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(iso_to_gmail_timestamp(end_date))
        print(query, params)
        cursor.execute(query, params)
        rows = cursor.fetchall()

        columns = ["id", "thread_id", "sender", "recipient", "subject", "timestamp", "body"]
        return [dict(zip(columns, row)) for row in rows]