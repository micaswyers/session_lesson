from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import sqlite3

DB = None
CONN = None

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

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

@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))

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

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug = True)
