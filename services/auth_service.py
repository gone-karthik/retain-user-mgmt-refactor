# services/auth_service.py
import sqlite3

DB_FILE = "users.db"

def verify_user_login(username: str, password: str) -> bool:
    """
    Fetch the stored password from the users table for the given username.
    Return True if passwords match, False otherwise.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False
