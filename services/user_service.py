import sqlite3

DB_FILE = "users.db"

def fetch_all_users():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users ORDER BY id")
        rows = cur.fetchall()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

def fetch_user_by_id(user_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
    return ({"id": row[0], "name": row[1], "email": row[2]} if row else None)

def search_users_by_name(name: str):
    term = f"%{name.strip().lower()}%"
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, email FROM users "
            "WHERE LOWER(name) LIKE ? ORDER BY id",
            (term,)
        )
        rows = cur.fetchall()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
