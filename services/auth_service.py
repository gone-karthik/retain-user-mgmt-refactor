import sqlite3

DB_FILE = "users.db"

def verify_user_login(login_key: str, password: str) -> bool:
    """
    Return True if a record exists with name, email, or username matching login_key (case-insensitive), and password matches.
    """

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Use parameterized queries (protects against SQL injection)
    try:
        cur.execute(
            """
            SELECT password
            FROM users
            WHERE LOWER(name) = LOWER(?)
               OR LOWER(email) = LOWER(?)
               OR LOWER(username) = LOWER(?)
            """,
            (login_key, login_key, login_key),
        )
    except sqlite3.OperationalError:
        # If there’s no 'username' column in the table, SQLite will throw; fallback to two-field version:
        cur.execute(
            """
            SELECT password
            FROM users
            WHERE LOWER(name) = LOWER(?)
               OR LOWER(email) = LOWER(?)
            """,
            (login_key, login_key),
        )

    row = cur.fetchone()
    conn.close()

    return bool(row and row[0] == password)
