from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "paperfile.db"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            title TEXT,
            year INTEGER,
            vita_type TEXT,
            journal_book TEXT,
            abstract TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    init_db()
    return render_template("index.html")


@app.route("/initdb")
def initdb():
    init_db()
    return "Database initialized."


@app.route("/addtest")
def addtest():
    init_db()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM papers")

    rows = [
        (
            "Bruce McCarl",
            "Climate Policy Analysis",
            2022,
            "Journal Articles",
            "Journal of Policy",
            "This paper analyzes the economic impacts of climate policy options."
        ),
        (
            "John Smith",
            "Agricultural Water Demand",
            2021,
            "Research Reports",
            "Water Economics Review",
            "This paper studies agricultural water demand and planning."
        ),
        (
            "Jane Doe",
            "Machine Learning in Agriculture",
            2024,
            "Journal Articles",
            "AI Agriculture Journal",
            "This paper explores machine learning in agriculture."
        ),
        (
            "Anay Kaundinya",
            "PM2.5 Effects on Plant Cells",
            2026,
            "Student Research",
            "Student Research Journal",
            "This study investigates PM2.5 effects on plant cells."
        )
    ]

    cursor.executemany("""
        INSERT INTO papers (author, title, year, vita_type, journal_book, abstract)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()

    return "Test data added."


@app.route("/search", methods=["POST"])
def search():
    author = request.form.get("author", "").strip()
    title = request.form.get("title", "").strip()

    conn = connect_db()
    cursor = conn.cursor()

    results = cursor.execute(
        """
        SELECT * FROM papers
        WHERE author LIKE ? AND title LIKE ?
        ORDER BY author, title
        """,
        (f"%{author}%", f"%{title}%")
    ).fetchall()

    conn.close()

    return render_template("results.html", results=results)


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)