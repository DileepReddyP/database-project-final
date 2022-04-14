from datetime import datetime
from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required

from server.models import Appointment, Patient, Role, User

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/")
def index():
    "login page"
    return render_template("login.html")


@pages.route("/admin")
@login_required
def admin_page():
    "admin page"
    if current_user.role == Role.ADMIN:
        users = User.query.all()
        return render_template("admin.html", users=users)
    return redirect("/")


@pages.route("/health/home")
@login_required
def health_home_page():
    "hmr page"
    if current_user.role == Role.NURSE:
        appointments = Appointment.query.all()
        completed = filter(lambda x: x.completed, appointments)
        not_completed = list(filter(lambda x: not x.completed, appointments))
        emergencies = filter(lambda x: x.emergency, not_completed)
        non_emergencies = filter(lambda x: not x.emergency, not_completed)
        patients = Patient.query.all()
        doctors = User.query.filter_by(role=Role.DOCTOR).all()
        return render_template(
            "nurse_home.html",
            completed=completed,
            emergencies=emergencies,
            non_emergencies=non_emergencies,
            patients=patients,
            doctors=doctors,
            today=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            user_id=current_user.id,
        )
    return redirect("/")


@pages.route("/doctor/home")
@login_required
def doctor_home_page():
    "hmr page"
    if current_user.role == Role.DOCTOR:
        appointments = Appointment.query.filter_by(doctor_id=current_user.id).all()
        completed = filter(lambda x: x.completed, appointments)
        not_completed = list(filter(lambda x: not x.completed, appointments))
        emergencies = filter(lambda x: x.emergency, not_completed)
        non_emergencies = filter(lambda x: not x.emergency, not_completed)
        return render_template(
            "nurse_home.html",
            completed=completed,
            emergencies=emergencies,
            non_emergencies=non_emergencies,
            user_id=current_user.id,
        )
    return redirect("/")
