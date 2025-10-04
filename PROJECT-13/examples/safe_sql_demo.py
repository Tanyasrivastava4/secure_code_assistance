# safe_sql_demo.py
# Secure version using parameterized queries (prevents SQL injection)
import sqlite3
import os

DB = "PROJECT-13/examples/demo_injection.db"

def setup():
    # If DB already exists from the vulnerable demo, we'll re-use it
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        c.executemany("INSERT INTO users (username, password) VALUES (?, ?)", [
            ("alice", "alicepass"),
            ("bob", "bobpass"),
        ])
        conn.commit()
        conn.close()

# safe query: use parameterized queries
def find_user_safe(user_input):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    sql = "SELECT id, username FROM users WHERE username = ?"
    print("Running SQL (parameterized):", sql, "with param:", user_input)
    c.execute(sql, (user_input,))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    setup()
    print("Database checked/created.\n")

    # normal search
    q = "alice"
    print("Normal query (alice):", find_user_safe(q))

    # same attack attempt
    inj = "' OR '1'='1"
    print("Injection attempt string:", inj)
    print("Result of injection on safe code:", find_user_safe(inj))
