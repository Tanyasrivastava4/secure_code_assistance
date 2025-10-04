# vulnerable_sql_demo.py
# Intentionally vulnerable demo for teaching only
import sqlite3
import os

DB = "PROJECT-13/examples/demo_injection.db"

# Setup DB and sample table
def setup():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.executemany("INSERT INTO users (username, password) VALUES (?, ?)", [
        ("alice", "alicepass"),
        ("bob", "bobpass"),
    ])
    conn.commit()
    conn.close()

# vulnerable query: concatenates user input directly
def find_user_vulnerable(raw_username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # VERY BAD: string concatenation -> allows SQL injection
    sql = f"SELECT id, username FROM users WHERE username = '{raw_username}'"
    print("Running SQL (vulnerable):", sql)
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    setup()
    print("Database created and sample users inserted.\n")

    # normal search
    q = "alice"
    print("Normal query (alice):", find_user_vulnerable(q))

    # attack attempt: classic injection to bypass WHERE
    inj = "' OR '1'='1"
    print("Injection attempt string:", inj)
    print("Result of injection on vulnerable code:", find_user_vulnerable(inj))
