import os
import smtplib
import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "travel.db"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

EMAIL_ADDRESS = "abrb270699@gmail.com"
EMAIL_PASSWORD = "broh awdk qoqw fcox"

# ---------------- DATABASE ----------------

def get_db():
    return sqlite3.connect(DATABASE)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")

# ---------------- DESTINATIONS ----------------

@app.route("/destinations")
def destinations():
    db = get_db()
    data = db.execute("SELECT * FROM destinations").fetchall()
    db.close()
    return render_template("destinations.html", destinations=data)



@app.route("/destination/<int:id>")
def destination_details(id):

    db = get_db()

    dest = db.execute(
        "SELECT * FROM destinations WHERE id=?",
        (id,)
    ).fetchone()

    images = db.execute(
        "SELECT image FROM destination_images WHERE destination_id=?",
        (id,)
    ).fetchall()

    packages = db.execute(
        "SELECT * FROM packages WHERE destination_id=?",
        (id,)
    ).fetchall()

    db.close()

    return render_template(
        "destination_details.html",
        dest=dest,
        images=images,
        packages=packages
    )

# ---------------- PACKAGES ----------------

@app.route("/packages")
def packages():
    search = request.args.get("search")

    db = get_db()
    if search:
        packages = db.execute("""
            SELECT packages.id, packages.title, packages.price,
                   destinations.name, packages.image
            FROM packages
            JOIN destinations
            ON packages.destination_id = destinations.id
            WHERE packages.title LIKE ?
        """, ('%' + search + '%',)).fetchall()
    else:
        packages = db.execute("""
            SELECT packages.id, packages.title, packages.price,
                   destinations.name, packages.image
            FROM packages
            JOIN destinations
            ON packages.destination_id = destinations.id
        """).fetchall()

    db.close()
    return render_template("packages.html", packages=packages)

# ---------------- BOOK PACKAGE ----------------

@app.route("/book/<int:id>", methods=["GET","POST"])
def book(id):

    if not session.get("user_id"):
        return redirect("/login")

    db = get_db()
    package = db.execute(
        "SELECT * FROM packages WHERE id=?",
        (id,)
    ).fetchone()
    db.close()

    if request.method == "POST":
        session["pending_booking"] = {
            "package_id": id,
            "name": request.form["name"],
            "email": request.form["email"]
        }
        return redirect("/payment")

    return render_template("booking.html", package=package)

# ---------------- SUCCESS ----------------

@app.route("/success")
def success():
    return render_template("success.html")

# ---------------- ADMIN LOGIN ----------------

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        db = get_db()
        admin = db.execute("""
            SELECT * FROM admins
            WHERE username=? AND password=?
        """,(u,p)).fetchone()
        db.close()

        if admin:
            session["admin"] = True
            return redirect("/dashboard")

    return render_template("admin_login.html")


# ---------------- USER REGISTER ----------------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        db = get_db()
        db.execute("""
            INSERT INTO users (name,email,password)
            VALUES (?,?,?)
        """,(name,email,hashed))
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("register.html")



# ---------------- USER LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("""
            SELECT * FROM users WHERE email=?
        """,(email,)).fetchone()
        db.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            next_page = request.args.get("next")
            return redirect(next_page or "/")

    return render_template("login.html")

# ---------------- USER LOGOUT ----------------
@app.route("/user_logout")
def user_logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    return redirect("/")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    db = get_db()
    packages = db.execute("""
    SELECT id, title, price
    FROM packages
    """).fetchall()

    destinations = db.execute("SELECT * FROM destinations").fetchall()
    bookings = db.execute("""
    SELECT bookings.id,
       customer_name,
       email,
       packages.title,
       destinations.name,
       payment_id,
       status,
       booking_date
    FROM bookings
    JOIN packages ON bookings.package_id = packages.id
    JOIN destinations ON packages.destination_id = destinations.id
    """).fetchall()

    db.close()

    return render_template("dashboard.html",
                           packages=packages,
                           bookings=bookings,
                           destinations=destinations)

# ---------------- ADD DESTINATION ----------------
@app.route("/add_destination", methods=["POST"])
def add_destination():

    name = request.form["name"]
    desc = request.form["description"]
    images = request.files.getlist("images")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO destinations(name,description)
        VALUES (?,?)
    """,(name,desc))

    dest_id = cur.lastrowid

    import uuid, os

    for img in images:
        filename = str(uuid.uuid4()) + "_" + img.filename
        img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        cur.execute("""
            INSERT INTO destination_images(destination_id,image)
            VALUES (?,?)
        """,(dest_id,filename))

    db.commit()
    db.close()

    return redirect("/dashboard")


@app.route("/delete_destination/<int:id>")
def delete_destination(id):
    db = get_db()
    db.execute("DELETE FROM destinations WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/dashboard")

# ---------------- ADD PACKAGE ----------------

@app.route("/add_package", methods=["POST"])
def add_package():
    title = request.form["title"]
    price = request.form["price"]
    dest = request.form["destination"]
    image = request.files["image"]

    filename = ""

    if image and image.filename != "":
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    db = get_db()
    db.execute("""
        INSERT INTO packages (title,price,destination_id,image)
        VALUES (?,?,?,?)
    """,(title,price,dest,filename))
    db.commit()
    db.close()

    return redirect("/dashboard")

@app.route("/edit_package/<int:id>", methods=["GET","POST"])
def edit_package(id):
    db = get_db()

    if request.method == "POST":
        title = request.form["title"]
        price = request.form["price"]

        db.execute("""
        UPDATE packages SET title=?, price=?
        WHERE id=?
        """,(title,price,id))
        db.commit()
        db.close()
        return redirect("/dashboard")

    package = db.execute("SELECT * FROM packages WHERE id=?", (id,)).fetchone()
    db.close()
    return render_template("edit_package.html", package=package)

@app.route("/edit_destination/<int:id>", methods=["GET","POST"])
def edit_destination(id):
    db = get_db()

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        db.execute("""
        UPDATE destinations SET name=?, description=?
        WHERE id=?
        """,(name,description,id))
        db.commit()
        db.close()
        return redirect("/dashboard")

    dest = db.execute("SELECT * FROM destinations WHERE id=?", (id,)).fetchone()
    db.close()
    return render_template("edit_destination.html", dest=dest)

# ---------------- DELETE PACKAGE ----------------

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM packages WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/dashboard")

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/payment", methods=["GET","POST"])
def payment():

    booking = session.get("pending_booking")

    if not booking:
        return redirect("/packages")

    if request.method == "POST":
        import uuid, datetime

        payment_id = "PAY" + str(uuid.uuid4())[:8]
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db = get_db()

        pkg = db.execute("""
        SELECT packages.title, packages.price, destinations.name
        FROM packages
        JOIN destinations ON packages.destination_id = destinations.id
        WHERE packages.id=?
        """,(booking["package_id"],)).fetchone()

        db.execute("""
            INSERT INTO bookings
            (customer_name,email,package_id,payment_id,status,booking_date)
            VALUES (?,?,?,?,?,?)
        """,(
            booking["name"],
            booking["email"],
            booking["package_id"],
            payment_id,
            "PAID",
            today
        ))

        db.commit()
        db.close()


        session.pop("pending_booking")
        return redirect("/success")

    return render_template("payment.html")




@app.route("/cancel_booking/<int:id>")
def cancel_booking(id):
    db = get_db()
    db.execute("""
        UPDATE bookings SET status='CANCELLED'
        WHERE id=?
    """,(id,))
    db.commit()
    db.close()
    return redirect("/dashboard")


@app.route("/export_bookings")
def export_bookings():

    db = get_db()
    data = db.execute("""
    SELECT customer_name,email,
           packages.title,
           destinations.name,
           payment_id,status,booking_date
    FROM bookings
    JOIN packages ON bookings.package_id = packages.id
    JOIN destinations ON packages.destination_id = destinations.id
    """).fetchall()
    db.close()

    df = pd.DataFrame(data, columns=[
        "Customer","Email","Package",
        "Destination","Payment ID",
        "Status","Date"
    ])

    df.to_excel("bookings.xlsx", index=False)
    return send_file("bookings.xlsx", as_attachment=True)



# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
