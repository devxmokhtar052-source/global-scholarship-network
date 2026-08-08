from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "change-this-to-a-random-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scholarships.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Scholarship(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    country = db.Column(db.String(100), nullable=False)

    university = db.Column(db.String(200))

    degree = db.Column(db.String(100))

    deadline = db.Column(db.String(50))

    description = db.Column(db.Text)

    benefits = db.Column(db.Text)

    eligibility = db.Column(db.Text)

    documents = db.Column(db.Text)

    apply_link = db.Column(db.String(500))
class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

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

if __name__ == "__main__":
    app.run(debug=True)