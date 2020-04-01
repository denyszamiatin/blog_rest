import pathlib
import sqlite3
from flask import render_template, request, redirect, url_for, flash, g
from . import app

DB_FILE = pathlib.Path(__file__).parents[1] / "data" / "db.sqlite3"
db = sqlite3.connect(DB_FILE)
db.execute("""create table if not exists posts (
    id integer primary key,
    title varchar,
    body text,
    pub_date date
)""")
db.close()


@app.before_request
def create_db():
    g.db = sqlite3.connect(DB_FILE, check_same_thread=True)


@app.teardown_request
def close_db(exc):
    if g.db is not None:
        g.db.close()


@app.route("/")
def index():
    cursor = g.db.execute("select title, body, pub_date from posts")
    posts = cursor.fetchall()
    return render_template("index.html", posts=posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    title = body = date = ""
    if request.method == 'POST':
        title = request.form.get("title", '')
        body = request.form.get("body", '')
        date = request.form.get("date", '')
        if title and body and date:
            g.db.execute("insert into posts (title, body, pub_date) values (?, ?, ?)", (title, body, date))
            g.db.commit()
            flash("Post has been added successfully")
            return redirect(url_for('index'))
        flash("Invalid data")
    return render_template("add.html", title=title, body=body, date=date)
