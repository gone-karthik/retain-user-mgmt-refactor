import sqlite3
from typing import Optional

# Should match the name and location of your SQLite DB file
DB_FILE = "users.db"

def verify_user_login(login_key: str, password: str) -> bool:
    """
    Return True if 'login_key' (name, email or username) exists
    and password matches; otherwise False.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Use placeholders to prevent SQL injection attacks
    # This is DB-API standard practice :contentReference[oaicite:0]{index=0}
    try:
        cur.execute(
            "SELECT password FROM users "
            "WHERE name = ? OR email = ? OR username = ?",
            (login_key, login_key, login_key),
        )
    except sqlite3.OperationalError:
        # If table has no 'username' column
        # gracefully downgrade to two-column version
        cur.execute(
            "SELECT password FROM users WHERE name = ? OR email = ?",
            (login_key, login_key),
        )

    row = cur.fetchone()
    conn.close()

    if not row:
        return False
    stored_password = row[0] or ""
    return password == stored_password
