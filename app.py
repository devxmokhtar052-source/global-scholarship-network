from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "change-this-to-a-random-secret-key"

app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scholarships.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Scholarship(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    country = db.Column(db.String(100), nullable=False)

    university = db.Column(db.String(200))

    degree = db.Column(db.String(100))

    deadline = db.Column(db.Date)

    description = db.Column(db.Text)

    benefits = db.Column(db.Text)

    eligibility = db.Column(db.Text)

    documents = db.Column(db.Text)

    apply_link = db.Column(db.String(500))
    image = db.Column(db.String(300))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
class Admin(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)

    scholarships = Scholarship.query.order_by(
    Scholarship.updated_at.desc()
    ).paginate(page=page, per_page=6)

    return render_template("home.html", scholarships=scholarships)

@app.route("/scholarship_details/<int:id>")
def scholarship_details(id):

    scholarship = Scholarship.query.get_or_404(id)

    return render_template(
        "scholarship_details.html",
        scholarship=scholarship
    )

@app.route("/scholarships")
def scholarships():
    scholarships = Scholarship.query.all()
    return render_template("scholarships.html", scholarships=scholarships)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            session["admin_id"] = admin.id

            return redirect(url_for("admin_dashboard"))

        return "Invalid username or password"

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()

    query = Scholarship.query

    if search:
        query = query.filter(
            db.or_(
                Scholarship.title.ilike(f"%{search}%"),
                Scholarship.country.ilike(f"%{search}%"),
                Scholarship.university.ilike(f"%{search}%"),
                Scholarship.degree.ilike(f"%{search}%")
            )
        )

    scholarships = query.order_by(
        Scholarship.updated_at.desc()
    ).all()

    return render_template(
    "admin_dashboard.html",
    scholarships=scholarships,
    today=datetime.today().date()
)

@app.route("/admin/scholarship/add", methods=["GET", "POST"])
def add_scholarship():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        image = request.files.get("image")

        image_filename = None

        if image and image.filename:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))


        scholarship = Scholarship(
            title=request.form["title"],
            country=request.form["country"],
            university=request.form["university"],
            degree=request.form["degree"],
            deadline=datetime.strptime(request.form["deadline"],"%Y-%m-%d").date(),
            description=request.form["description"],
            benefits=request.form["benefits"],
            eligibility=request.form["eligibility"],
            documents=request.form["documents"],
            apply_link=request.form["apply_link"],
            image=image_filename
        )

        db.session.add(scholarship)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_scholarship.html")

@app.route("/admin/scholarship/edit/<int:id>", methods=["GET", "POST"])
def edit_scholarship(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    scholarship = Scholarship.query.get_or_404(id)

    if request.method == "POST":

        scholarship.title = request.form["title"]
        scholarship.country = request.form["country"]
        scholarship.university = request.form["university"]
        scholarship.degree = request.form["degree"]
        scholarship.deadline = datetime.strptime(request.form["deadline"],"%Y-%m-%d").date()
        scholarship.description = request.form["description"]
        scholarship.benefits = request.form["benefits"]
        scholarship.eligibility = request.form["eligibility"]
        scholarship.documents = request.form["documents"]
        scholarship.apply_link = request.form["apply_link"]

        image = request.files.get("image")

        if image and image.filename:
            image_filename = secure_filename(image.filename)
            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    image_filename
                )
            )
            scholarship.image = image_filename

        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template(
        "edit_scholarship.html",
        scholarship=scholarship
    )

@app.route("/admin/scholarship/delete/<int:id>")
def delete_scholarship(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    scholarship = Scholarship.query.get_or_404(id)

    if scholarship.image:
        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            scholarship.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(scholarship)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_id", None)

    return redirect(url_for("admin_login"))

@app.after_request
def add_no_cache_headers(response):

    if request.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response

if __name__ == "__main__":
    app.run(debug=True)