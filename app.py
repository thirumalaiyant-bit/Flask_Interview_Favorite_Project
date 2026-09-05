
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("favorites.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db()
    favorites = conn.execute("SELECT * FROM favorites").fetchall()
    conn.close()
    return render_template("index.html", favorites=favorites)

@app.route("/add", methods=["GET", "POST"])
def add_favorite():
    if request.method == "POST":
        name = request.form["name"]
        favorite = request.form["favorite"]

        conn = get_db()
        conn.execute(
            "INSERT INTO favorites (name, favorite) VALUES (?, ?)",
            (name, favorite)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete_favorite(id):
    conn = get_db()
    conn.execute("DELETE FROM favorites WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
