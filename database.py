import sqlite3

DB = "history.db"

# ---------- CONNECTION ----------
def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)


# ---------- CREATE TABLES ----------
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS searches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        stock TEXT,
        price REAL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ---------- REGISTER ----------
def create_user(username, password):
    try:
        conn = get_conn()
        c = conn.cursor()

        c.execute("INSERT INTO users(username,password) VALUES (?,?)",
                  (username, password))

        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


# ---------- LOGIN ----------
def check_user(username, password):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))

    user = c.fetchone()
    conn.close()
    return user


# ---------- SAVE SEARCH ----------
def save_search(username, stock, price):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        "INSERT INTO searches(username,stock,price) VALUES (?,?,?)",
        (str(username), str(stock), float(price))
    )

    conn.commit()
    conn.close()


# ---------- HISTORY ----------
def get_history(username):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT stock, price, time
        FROM searches
        WHERE username=?
        ORDER BY id DESC
        LIMIT 5
    """, (username,))

    rows = c.fetchall()
    conn.close()
    return rows
