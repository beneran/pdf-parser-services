import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_db(db_path='reports.db'):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                grade TEXT NOT NULL,
                semester TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, subject, semester)
        ''')
        conn.commit()
        logger.info(f"Database initialized at {db_path}")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
    finally:
        conn.close()

def save_to_database(data, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for item in data:
            cursor.execute('''
                INSERT OR REPLACE INTO reports 
                (student_id, student_name, subject, grade, semester)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item.get('student_id', ''),
                item.get('student_name', ''),
                item.get('subject', ''),
                item.get('grade', ''),
                item.get('semester', '')
            ))
        
        conn.commit()
        logger.info(f"Saved {len(data)} records to database")
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        conn.close()