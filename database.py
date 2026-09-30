import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "applications.db")

def get_connection():
    """Returns a connection instance to the applications.db SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes schema and runs automatic migration checks for missing columns."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Base table creation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                date_applied TEXT,
                location TEXT,
                job_url TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Schema Migration: Check existing columns to dynamically alter older tables
        cursor.execute("PRAGMA table_info(applications)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        required_columns = {
            "location": "TEXT",
            "job_url": "TEXT",
            "notes": "TEXT",
            "date_applied": "TEXT",
            "status": "TEXT DEFAULT 'Applied'"
        }
        
        for col_name, col_type in required_columns.items():
            if col_name not in existing_columns:
                cursor.execute(f"ALTER TABLE applications ADD COLUMN {col_name} {col_type}")
                
        conn.commit()

# Ensure schema and migrations run on module import
init_db()

def add_application(
    company: str, 
    role: str, 
    status: str = "Applied", 
    date_applied: str = "", 
    location: str = "", 
    job_url: str = "", 
    notes: str = ""
) -> int:
    """Inserts a new job application record into SQLite."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO applications (company, role, status, date_applied, location, job_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (company, role, status, date_applied, location, job_url, notes)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_applications() -> List[Dict[str, Any]]:
    """Retrieves all logged job applications sorted by application date."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications ORDER BY date_applied DESC, id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_application_stats() -> Dict[str, int]:
    """Calculates KPI statistics across recruitment stages for the dashboard."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM applications GROUP BY status")
        rows = cursor.fetchall()
        
        stats = {
            "total": 0,
            "applied": 0,
            "interviewing": 0,
            "offered": 0,
            "rejected": 0
        }
        
        for row in rows:
            st_name = str(row["status"]).strip().lower()
            count = row["count"]
            stats["total"] += count
            
            if st_name in ["applied"]:
                stats["applied"] += count
            elif st_name in ["interviewing", "interview"]:
                stats["interviewing"] += count
            elif st_name in ["offer", "offered"]:
                stats["offered"] += count
            elif st_name in ["rejected"]:
                stats["rejected"] += count

        return stats

def update_application_status(app_id: int, new_status: str) -> None:
    """Updates the recruitment stage for a given application ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (new_status, app_id)
        )
        conn.commit()
        
def delete_application(app_id: int) -> None:
    """Deletes an application record by ID from SQLite."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()