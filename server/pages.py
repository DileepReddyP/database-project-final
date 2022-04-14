from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required

from server.models import Patient, Role, User

pages = Blueprint("pages", __name__, template_folder='templates')

@pages.route('/')
def index():
    "login page"
    return render_template("login.html")

@pages.route('/admin')
@login_required
def admin_page():
    "admin page"
    if current_user.role == Role.ADMIN:
        users = User.query.all()
        return render_template("admin.html", users=users)
    return redirect("/")

@pages.route('/health/home')
@login_required
def health_home_page():
    "hmr page"
    if current_user.role == Role.NURSE:
        patients = Patient.query.all()
        return render_template("nurse_home.html", patients=patients)
    return redirect("/")