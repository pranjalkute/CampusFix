from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home / Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@gmail.com" and password == "admin123":
            session["role"] = "admin"
            return redirect("/admin")

        elif email == "student@gmail.com" and password == "student123":
            session["role"] = "student"
            return redirect("/dashboard")

    return render_template("login.html")


# Student dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Report issue
@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        issue = request.form["issue"]
        photo = request.files["photo"]

        path = os.path.join(UPLOAD_FOLDER, photo.filename)
        photo.save(path)

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO reports(issue, photo, status) VALUES (?, ?, ?)",
                    (issue, path, "Pending"))
        con.commit()
        con.close()

        return "Report Submitted"

    return render_template("report.html")


# Admin panel
@app.route("/admin", methods=["GET", "POST"])
def admin():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    if request.method == "POST":
        rid = request.form["id"]
        status = request.form["status"]
        cur.execute("UPDATE reports SET status=? WHERE id=?", (status, rid))
        con.commit()

    cur.execute("SELECT * FROM reports")
    data = cur.fetchall()
    con.close()

    return render_template("admin.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
