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
    if hash(password) == row[2]:
        return row[1]

def get_user_by_name(username):
    query = """SELECT * FROM users WHERE username = ?"""
    DB.execute(query, (username, ))
    rows = DB.fetchall()
    return rows[0]

def get_wall_posts(user_id):
    query = """SELECT * FROM wall_posts WHERE id = ?"""
    DB.execute(query, (user_id, ))
    rows = DB.fetchall()
    return rows