import sqlite3

DB_FILE = "users.db"

def verify_user_login(login_key: str, password: str) -> bool:
    """
    Returns True if a user with this login_key (email or username)
    exists and the password matches.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        # Parameterized query protects against SQL injection
        try:
            cur.execute(
                "SELECT password FROM users WHERE username = ? OR email = ?",
                (login_key, login_key)
            )
        except sqlite3.OperationalError:
            # 'username' column may not exist; try only email
            cur.execute("SELECT password FROM users WHERE email = ?", (login_key,))
        row = cur.fetchone()

    if not row:
        return False
    return row[0] == password
