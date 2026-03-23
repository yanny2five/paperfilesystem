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
            "Economic Impacts of Climate Policy Instruments",
            2022,
            "Journal Articles",
            "Journal of Environmental Economics",
            "This paper evaluates the economic effects of different climate policy instruments, including carbon taxes and cap-and-trade systems."
        ),
        (
            "Michael Green",
            "Agricultural Water Demand Under Climate Variability",
            2021,
            "Research Reports",
            "Water Resources Review",
            "This study analyzes how climate variability influences agricultural water demand and resource allocation."
        ),
        (
            "Sarah Johnson",
            "Machine Learning Approaches for Crop Yield Prediction",
            2024,
            "Journal Articles",
            "Computational Agriculture Journal",
            "This paper explores the application of machine learning models to improve crop yield predictions and agricultural decision-making."
        ),
        (
            "David Lee",
            "Energy Market Responses to Environmental Regulation",
            2020,
            "Book Chapters",
            "Energy Economics Handbook",
            "This chapter examines how energy markets respond to environmental regulations and policy changes."
        ),
        (
            "Emily Chen",
            "Sustainable Land Use and Policy Optimization",
            2023,
            "Journal Articles",
            "Land Use Policy Journal",
            "This paper investigates strategies for optimizing land use under sustainability and policy constraints."
        ),
        (
            "Robert Wilson",
            "Economic Modeling of Food Supply Chains",
            2019,
            "Research Reports",
            "Agricultural Systems Review",
            "This study models food supply chains to analyze efficiency, resilience, and economic impacts."
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