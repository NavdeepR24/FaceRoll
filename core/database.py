import sqlite3
from datetime import datetime, date
import pandas as pd

DB_PATH = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        roll_no TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        branch TEXT,
        email TEXT,
        registered_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        name TEXT,
        date TEXT,
        time TEXT,
        status TEXT DEFAULT 'Present'
    )''')
    conn.commit()
    conn.close()

def add_student(roll_no, name, branch, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO students VALUES (?,?,?,?,?)",
              (roll_no, name, branch, email, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def mark_attendance(roll_no, name):
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Mark only once per day
    c.execute("SELECT id FROM attendance WHERE roll_no=? AND date=?", (roll_no, today))
    if not c.fetchone():
        c.execute("INSERT INTO attendance (roll_no, name, date, time) VALUES (?,?,?,?)",
                  (roll_no, name, today, now))
        conn.commit()
        conn.close()
        return True   # newly marked
    conn.close()
    return False      # already marked

def get_today_attendance():
    conn = sqlite3.connect(DB_PATH)
    today = date.today().isoformat()
    df = pd.read_sql_query(
        "SELECT * FROM attendance WHERE date=?", conn, params=(today,)
    )
    conn.close()
    return df

def get_all_attendance():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM attendance ORDER BY date DESC, time DESC", conn)
    conn.close()
    return df

def get_all_students():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    add_student("CS001", "Raj Kumar", "CSE", "raj@email.com")
    mark_attendance("CS001", "Raj Kumar")
    mark_attendance("CS001", "Raj Kumar")  # should NOT duplicate

    print("=== Students ===")
    print(get_all_students())

    print("=== Attendance ===")
    print(get_all_attendance())

    print("=== Today ===")
    print(get_today_attendance())