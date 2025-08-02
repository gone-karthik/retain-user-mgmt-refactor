import sqlite3

DB_FILE = "users.db"

def fetch_all_users():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users")
    results = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in results
    ]

def fetch_user_by_id(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2]}
    return None

def search_users_by_name(name_str: str):
    name_lower = f"%{name_str.lower()}%"
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, email FROM users WHERE LOWER(name) LIKE ?",
        (name_lower,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ]
