import sqlite3

def connect_db():
    return sqlite3.connect("resumatch.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            role TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            score INTEGER,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_resume(file_name, role, matched, missing, score):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resumes (file_name, role, matched_skills, missing_skills, score)
        VALUES (?, ?, ?, ?, ?)
    """, (file_name, role, ", ".join(matched), ", ".join(missing), score))
    conn.commit()
    conn.close()

def fetch_all_resumes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes ORDER BY upload_time DESC")
    data = cursor.fetchall()
    conn.close()
    return data
