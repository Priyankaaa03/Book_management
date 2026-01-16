from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

from flask import Flask
app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "booksecret"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    return render_template("dashboard.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        data = (
            request.form["name"],
            request.form["author"],
            request.form["price"],
            request.form["qty"]
        )
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO books(name, author, price, qty) VALUES (?, ?, ?, ?)", data
        )
        db.commit()
        return redirect("/dashboard")
    return render_template("add_book.html")

@app.route("/delete/<int:id>")
def delete_book(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT,
        price REAL,
        qty INTEGER
    )
    """)
    db.close()
    app.run(debug=True)
