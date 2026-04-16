from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("cakeshop.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db()
    cakes = conn.execute("SELECT * FROM cakes").fetchall()
    conn.close()
    return render_template("home.html", cakes=cakes)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        conn = get_db()
        conn.execute("""
            INSERT INTO cakes (name, price, image, stock)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["name"],
            request.form["price"],
            request.form["image"],
            request.form["stock"]
        ))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()

    if request.method == "POST":
        conn.execute("""
            UPDATE cakes
            SET name=?, price=?, image=?, stock=?
            WHERE id=?
        """, (
            request.form["name"],
            request.form["price"],
            request.form["image"],
            request.form["stock"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/")

    cake = conn.execute("SELECT * FROM cakes WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", cake=cake)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM cakes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)