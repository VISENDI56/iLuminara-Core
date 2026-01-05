import sqlite3
import os
from datetime import datetime

class InstitutionalDatabase:
    def __init__(self, db_path="iluminara-nexus/data/sovereign_records.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.initialize_db()

    def initialize_db(self):
        """Initializes the SQLite schema for humanitarian records."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT,
                location TEXT,
                symptom_code TEXT,
                severity_score INTEGER,
                timestamp TEXT,
                sync_status TEXT DEFAULT 'LOCAL_ONLY'
            )
        ''')
        conn.commit()
        conn.close()

    def save_signal(self, signal_obj):
        """Commits a validated signal to persistent local storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO health_signals (source_id, location, symptom_code, severity_score, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (signal_obj.source_id, signal_obj.location, signal_obj.symptom_code, 
              signal_obj.severity_score, signal_obj.timestamp))
        conn.commit()
        conn.close()

    def get_recent_signals(self, limit=5):
        """Retrieves recent records for UI display."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM health_signals ORDER BY id DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows
