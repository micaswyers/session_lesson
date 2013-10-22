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
        return "Yay, it worked!"
    else:
        return render_template('index.html')

@app.route("/user/<username>")
def view_user(username):
    owner_id = model.get_user_by_name(username)
    print owner_id
    user_wall_posts = model.get_wall_posts(owner_id)
    print user_wall_posts
    return render_template("wall.html", posts=user_wall_posts)

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
