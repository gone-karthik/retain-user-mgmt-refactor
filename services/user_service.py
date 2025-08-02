import sqlite3

DB_FILE = "users.db"

def fetch_all_users():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

def fetch_user_by_id(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return {"id": row[0], "name": row[1], "email": row[2]} if row else None

def search_users_by_name(q: str):
    q = q.strip()
    if not q:
        return []
    pattern = f"%{q.lower()}%"
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, email FROM users WHERE LOWER(name) LIKE ? ORDER BY id",
        (pattern,),
    )
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
