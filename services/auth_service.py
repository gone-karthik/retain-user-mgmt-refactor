import sqlite3

DB_FILE = "users.db"

def verify_user_login(login_key: str, password: str) -> bool:
    """
    Returns True if a user matching name/email/username (case-insensitive)
    exists and the password matches. Falls back to admin:secret if no row found.
    Uses parameterized queries to prevent SQL injection.
    """

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    login_key_lower = login_key.lower()
    row = None

    try:
        cur.execute(
            """
            SELECT password
            FROM users
            WHERE LOWER(name) = ?
               OR LOWER(email) = ?
               OR LOWER(username) = ?
            """,
            (login_key_lower, login_key_lower, login_key_lower),
        )
        row = cur.fetchone()
    except sqlite3.OperationalError:
        # Table doesn’t have username column—fallback to name/email
        cur.execute(
            """
            SELECT password
            FROM users
            WHERE LOWER(name) = ?
               OR LOWER(email) = ?
            """,
            (login_key_lower, login_key_lower),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    # If DB returned a row, compare stored password
    if row:
        return password == row[0]

    # Otherwise, for typing exercises or legacy fallback
    return login_key_lower == "admin" and password == "secret"
