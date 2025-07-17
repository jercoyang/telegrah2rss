import sqlite3
from contextlib import closing
import os

def get_db_connection():
    return sqlite3.connect('rss_jobs.db', check_same_thread=False)

def init_db():
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rss_jobs (
                uid TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        conn.commit()

def save_job(uid, url, job_type):
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO rss_jobs (uid, url, type)
            VALUES (?, ?, ?)
        ''', (uid, url, job_type))
        conn.commit()

def load_jobs():
    jobs = {}
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT uid, url FROM rss_jobs')
            for uid, url in cursor.fetchall():
                jobs[uid] = url
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            init_db()
            return load_jobs()
        else:
            print(f"Database error: {e}")
    return jobs