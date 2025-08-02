import sqlite3

DB_FILE = "users.db"

def fetch_all_users():
    """Return a list of all users with id, name, and email."""
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        # Safe parameterized query (no injection risk)
        cur.execute("SELECT id, name, email FROM users")
        rows = cur.fetchall()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

def fetch_user_by_id(user_id: int):
    """Return a single user dict or None if not found."""
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
    if not row:
        return None
    return {"id": row[0], "name": row[1], "email": row[2]}

def search_users_by_name(q: str):
    """Case-insensitive search for any substring in name."""
    pattern = f"%{q.strip().lower()}%"
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE LOWER(name) LIKE ?", (pattern,))
        rows = cur.fetchall()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
