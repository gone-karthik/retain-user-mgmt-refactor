import sqlite3
from typing import Any, Dict, List, Optional
from datetime import datetime

DB_FILE = "users.db"

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def health_check() -> str:
    return "OK"

def fetch_user(user_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()

    # Parameter substitution avoids SQL injection
    cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None
    return dict(row)

def fetch_all_users() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def search_users(name_filter: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    like_term = f"%{name_filter}%"
    cur.execute("SELECT id, name, email FROM users WHERE name LIKE ? ORDER BY id", (like_term,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_user(body: Dict[str, Any]) -> Dict[str, Any]:
    name = body.get("name")
    email = body.get("email")
    password = body.get("password")

    if not name or not email or not password:
        raise ValueError("name, email and password are required")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, ?)",
        (name, email, password, datetime.utcnow().isoformat()),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": str(new_id), "name": name, "email": email}

def update_user(user_id: str, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    name = body.get("name")
    email = body.get("email")
    password = body.get("password")

    if not name and not email and not password:
        raise ValueError("nothing to update")

    conn = get_db_connection()
    cur = conn.cursor()

    fields = []
    params = []
    if name:
        fields.append("name = ?")
        params.append(name)
    if email:
        fields.append("email = ?")
        params.append(email)
    if password:
        fields.append("password = ?")
        params.append(password)

    params.append(user_id)
    sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    cur.execute(sql, tuple(params))
    conn.commit()

    # Check if any row actually updated
    if cur.rowcount == 0:
        conn.close()
        return None

    cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row)

def delete_user(user_id: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = (cur.rowcount == 1)
    conn.close()
    return deleted
