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
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username, ))
    row = DB.fetchone()
    return row[0]

def get_wall_posts(owner_id):
    connect_to_db()
    query = """SELECT wp.id, wp.author_id, u.username, wp.content, wp.created_at FROM wall_posts as wp INNER JOIN users as u on (wp.author_id = u.id) WHERE owner_id = ?"""
    DB.execute(query, (owner_id, ))
    rows = DB.fetchall()
    output = []
    for row in rows:
        row_d = {"username": row[2],
                 "content": row[3],
                 "date": row[4] }
        output.append(row_d)
    print rows

    # list comprehension
    # output = [ {"username": row[2], "content": row[3], "date": row[4]} for row in rows ]
    return output

def post_to_wall(owner_id, author_id, created_at, content):
    connect_to_db()
    query = """INSERT INTO wall_posts (owner_id, author_id, created_at, content) VALUES (?, ?, ?, ?)"""
    DB.execute(query, (owner_id, author_id, created_at, content))
    CONN.commit()
    print "Posted to wall %s %s %s %s" % (owner_id, author_id, created_at, content)