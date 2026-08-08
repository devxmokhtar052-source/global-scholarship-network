from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scholarship_details")
def scholarship_details():
    return render_template("scholarship_details.html")

@app.route("/scholarships")
def scholarships():
    return render_template("scholarships.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)