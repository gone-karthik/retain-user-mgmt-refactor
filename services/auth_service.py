import sqlite3

DB_FILE = "users.db"

def verify_user_login(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    stored_password = row[0]
    return password == stored_password  # plaintext matches legacy behavior
