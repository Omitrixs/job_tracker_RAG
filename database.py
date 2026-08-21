import sqlite3
import os
from models import Application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "applications.db")

class Tracker:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    status TEXT NOT NULL,
                    date_applied TEXT NOT NULL,
                    notes TEXT
                )
            """)
            conn.commit()

    def add_application(self, app: Application):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO applications (company, role, status, date_applied, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (app.company, app.role, app.status, app.date_applied, app.notes))
            conn.commit()
            print(f"\n[Success] App record saved with ID #{cursor.lastrowid}")

    def get_all_applications(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, company, role, status, date_applied, notes FROM applications")
            rows = cursor.fetchall()
            return [Application(company=r[1], role=r[2], status=r[3], date_applied=r[4], notes=r[5], app_id=r[0]) for r in rows]

    def get_followup_reminders(self, threshold_days=14):
        apps = self.get_all_applications()
        return [app for app in apps if app.status == "applied" and app.days_since_applied() >= threshold_days]