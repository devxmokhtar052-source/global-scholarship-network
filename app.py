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
    how_to_apply = db.Column(db.Text)

    documents = db.Column(db.Text)
    how_to_apply = db.Column(db.Text)

    opportunity_type = db.Column(db.Text)
    language_requirement = db.Column(db.String(50))

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

    # Existing latest opportunities section - DO NOT CHANGE
    scholarships = Scholarship.query.order_by(
        Scholarship.updated_at.desc()
    ).paginate(page=page, per_page=6)

    # Latest 3 by opportunity
    masters_scholarships = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%Master's%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    phd_scholarships = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%PhD%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    undergraduate_scholarships = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%Undergraduate%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    postdoctoral_scholarships = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%Postdoctoral%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    internships = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%Internship%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    fellowships = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%Fellowship%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    exchange_programs = Scholarship.query.filter(
        Scholarship.opportunity_type.ilike("%Exchange Program%")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    # Latest 3 by region
    usa_scholarships = Scholarship.query.filter(
        Scholarship.country.in_(["United States"])
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    china_scholarships = Scholarship.query.filter(
        Scholarship.country.ilike("China")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    japan_scholarships = Scholarship.query.filter(
        Scholarship.country.ilike("Japan")
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    middle_east_scholarships = Scholarship.query.filter(
        Scholarship.country.in_([
            "Bahrain",
            "Iran",
            "Iraq",
            "Jordan",
            "Kuwait",
            "Lebanon",
            "Oman",
            "Qatar",
            "Saudi Arabia",
            "United Arab Emirates"
        ])
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    europe_scholarships = Scholarship.query.filter(
        Scholarship.country.in_([
            "Albania",
            "Austria",
            "Belgium",
            "Bulgaria",
            "Croatia",
            "Cyprus",
            "Czech Republic",
            "Denmark",
            "Estonia",
            "Finland",
            "France",
            "Germany",
            "Greece",
            "Hungary",
            "Iceland",
            "Ireland",
            "Italy",
            "Latvia",
            "Lithuania",
            "Luxembourg",
            "Malta",
            "Netherlands",
            "Norway",
            "Poland",
            "Portugal",
            "Romania",
            "Serbia",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden",
            "Switzerland",
            "Türkiye",
            "Ukraine",
            "United Kingdom"
        ])
    ).order_by(
        Scholarship.updated_at.desc()
    ).limit(3).all()

    return render_template(
        "home.html",
        scholarships=scholarships,

        masters_scholarships=masters_scholarships,
        phd_scholarships=phd_scholarships,
        undergraduate_scholarships=undergraduate_scholarships,
        postdoctoral_scholarships=postdoctoral_scholarships,
        internships=internships,
        fellowships=fellowships,
        exchange_programs=exchange_programs,

        usa_scholarships=usa_scholarships,
        china_scholarships=china_scholarships,
        japan_scholarships=japan_scholarships,
        middle_east_scholarships=middle_east_scholarships,
        europe_scholarships=europe_scholarships
    )

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
    return render_template(
        "scholarships.html",
        scholarships=scholarships,
        category_heading="Latest Opportunities"
    )

@app.route("/scholarships/category/<category_type>/<path:category_value>")
def scholarship_category(category_type, category_value):
    category_heading = category_value
    if category_type == "region":
        category_heading = f"Scholarships in {category_value}"

    elif category_type == "opportunity":

        if category_value == "Internship":
            category_heading = "Internships"

        elif category_value == "Fellowship":
            category_heading = "Fellowships"

        elif category_value == "Exchange Program":
            category_heading = "Exchange Programs"

        elif category_value == "Master's":
            category_heading = "Master's Scholarships"

        elif category_value == "PhD":
            category_heading = "PhD Scholarships"

        elif category_value == "Undergraduate":
            category_heading = "Undergraduate Scholarships"

        elif category_value == "Postdoctoral":
            category_heading = "Postdoctoral Scholarships"

        elif category_value == "Diploma / Certificate":
            category_heading = "Diploma / Certificate Scholarships"

        else:
            category_heading = f"{category_value} Opportunities"

    elif category_type == "language":

        if category_value == "IELTS":
            category_heading = "IELTS Scholarships"

        elif category_value == "No IELTS":
            category_heading = "No IELTS Scholarships"

        else:
            category_heading = f"{category_value} Scholarships"
    if category_type == "region":
        region_groups = {
            "Europe": [
                "Albania", "Austria", "Belgium", "Bulgaria", "Croatia",
                "Cyprus", "Czech Republic", "Denmark", "Estonia",
                "Finland", "France", "Germany", "Greece", "Hungary",
                "Iceland", "Ireland", "Italy", "Latvia", "Lithuania",
                "Luxembourg", "Malta", "Netherlands", "Norway", "Poland",
                "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia",
                "Spain", "Sweden", "Switzerland", "Türkiye", "Ukraine",
                "United Kingdom"
            ],

            "Middle East": [
                "Bahrain", "Iran", "Iraq", "Jordan", "Kuwait",
                "Lebanon", "Oman", "Qatar", "Saudi Arabia",
                "United Arab Emirates"
            ],

            "USA": [
                "United States"
            ]
        }

        if category_value in region_groups:
            scholarships = Scholarship.query.filter(
                Scholarship.country.in_(region_groups[category_value])
            ).all()
        else:
            scholarships = Scholarship.query.filter(
                Scholarship.country.ilike(category_value)
            ).all()

    elif category_type == "opportunity":
        scholarships = Scholarship.query.filter(
            Scholarship.opportunity_type.ilike(f"%{category_value}%")
        ).all()

    elif category_type == "language":
        scholarships = Scholarship.query.filter(
            Scholarship.language_requirement.ilike(category_value)
        ).all()

    else:
        return "Invalid category", 404

    return render_template(
    "scholarships.html",
    scholarships=scholarships,
    category_heading=category_heading
)

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
            opportunity_type=", ".join(request.form.getlist("opportunity_type")),
            language_requirement=request.form.get("language_requirement"),
            deadline=datetime.strptime(request.form["deadline"],"%Y-%m-%d").date(),
            description=request.form["description"],
            benefits=request.form["benefits"],
            eligibility=request.form["eligibility"],
            documents=request.form["documents"],
            how_to_apply=request.form["how_to_apply"],
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
        scholarship.opportunity_type = ", ".join(request.form.getlist("opportunity_type"))
        scholarship.language_requirement = request.form.get("language_requirement")
        scholarship.deadline = datetime.strptime(request.form["deadline"],"%Y-%m-%d").date()
        scholarship.description = request.form["description"]
        scholarship.benefits = request.form["benefits"]
        scholarship.eligibility = request.form["eligibility"]
        scholarship.documents = request.form["documents"]
        scholarship.how_to_apply = request.form["how_to_apply"]
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

@app.route("/admin/scholarship/share/<int:id>")
def share_scholarship(id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    scholarship = Scholarship.query.get_or_404(id)

    return render_template(
        "share_scholarship.html",
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