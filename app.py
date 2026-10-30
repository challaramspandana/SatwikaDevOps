
import os
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "petcare-dev-secret"),
        DATABASE=os.environ.get(
            "DATABASE_PATH",
            str(Path(app.instance_path) / "pets.db")
        )
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    init_db(app)

    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    @app.route("/")
    def home():
        pets = [
            {
                "name": "Bruno",
                "type": "Dog",
                "age": "2 years",
                "gender": "Male",
                "description": "Friendly Golden Retriever.",
                "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=700"
            },
            {
                "name": "Luna",
                "type": "Cat",
                "age": "1 year",
                "gender": "Female",
                "description": "Calm and affectionate cat.",
                "image": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=700"
            },
            {
                "name": "Max",
                "type": "Dog",
                "age": "6 months",
                "gender": "Male",
                "description": "Energetic and playful puppy.",
                "image": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=700"
            }
        ]

        return render_template("index.html", pets=pets)

    @app.route("/adopt", methods=["POST"])
    def adopt():
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        pet = request.form.get("pet", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, phone, pet]):
            flash("Please complete all required adoption fields.", "error")
            return redirect(url_for("home") + "#adoption")

        with get_db() as conn:
            conn.execute(
                """INSERT INTO adoptions
                (name, email, phone, pet, message)
                VALUES (?, ?, ?, ?, ?)""",
                (name, email, phone, pet, message)
            )

        flash("Your adoption request has been submitted successfully!", "success")
        return redirect(url_for("home") + "#adoption")

    @app.route("/rescue", methods=["POST"])
    def rescue():
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        location = request.form.get("location", "").strip()
        animal = request.form.get("animal", "").strip()
        condition = request.form.get("condition", "").strip()

        if not all([name, phone, location, animal, condition]):
            flash("Please complete all required rescue report fields.", "error")
            return redirect(url_for("home") + "#rescue")

        with get_db() as conn:
            conn.execute(
                """INSERT INTO rescues
                (name, phone, location, animal, condition)
                VALUES (?, ?, ?, ?, ?)""",
                (name, phone, location, animal, condition)
            )

        flash("Your rescue report has been submitted successfully!", "success")
        return redirect(url_for("home") + "#rescue")

    return app


def init_db(app):
    database = Path(app.config["DATABASE"])
    database.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS adoptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                pet TEXT NOT NULL,
                message TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS rescues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                location TEXT NOT NULL,
                animal TEXT NOT NULL,
                condition TEXT NOT NULL
            )
        """)


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
