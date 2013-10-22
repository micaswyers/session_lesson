import sqlite3

DB = None
CONN = None

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    connect_to_db()
    query = """SELECT * FROM users WHERE username = ?"""
    DB.execute(query, (username, ))
    row = DB.fetchone()
    if password == row[2]:
        return row[1]

def get_user_by_name(username):
    connect_to_db()
    query = """SELECT * FROM users WHERE username = ?"""
    DB.execute(query, (username, ))
    row = DB.fetchone()
    return row[0]

def get_wall_posts(owner_id):
    connect_to_db()
    query = """SELECT * FROM wall_posts WHERE owner_id = ?"""
    DB.execute(query, (owner_id, ))
    rows = DB.fetchall()
    print rows
    return rows