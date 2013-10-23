from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import sqlite3
import datetime

DB = None
CONN = None

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

# handler one
@app.route("/")
def index():
    if session.get('username'):
        username = session.get('username')
        return redirect(url_for("view_user", username=username))
    else:
        return render_template('index.html')

@app.route("/user/<username>")
def view_user(username):
    owner_id = model.get_user_by_name(username)
    user_wall_posts = model.get_wall_posts(owner_id)
    logged_in = session.get('username') #logged_in should be equal to a username
    print logged_in
    return render_template("wall.html", posts=user_wall_posts, logged_in=logged_in)


# handler two
@app.route("/", methods=["POST"]) 
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")
    username = model.authenticate(username, password)

    if username != None:
        flash("User authenticated!")
        session["username"] = username
        return redirect(url_for("view_user", username=username))

    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")
    return redirect(url_for("index"))


@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))

@app.route("/post_to_wall", methods=["POST"])
def post_to_wall():
    username = session.get('username')
    print "THIS IS THE USERNAME", username
    user_id = model.get_user_by_name(username)
    content = request.form.get('wall_posts')
    created_at = datetime.datetime.now()
    author_name = session.get('username')
    author_id = model.get_user_by_name(author_name)
    model.post_to_wall(user_id, author_id, created_at, content)

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug = True)