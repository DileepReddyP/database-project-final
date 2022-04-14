import random
import string
from time import strptime, strftime
from flask import Blueprint, redirect, request, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user

from server.models import Appointment, Medication, Patient, Prescription, Report, User, db, Role

api = Blueprint("api", __name__)


@api.route("/api/login", methods=["POST"])
def login_api():
    "login api"
    email = request.form.get("email")
    password = request.form.get("password")
    db.session.begin()
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Email is not recognized")
        return redirect(request.referrer)
    if not password == user.password:
        flash("Incorrect Password")
        return redirect(request.referrer)
    login_user(user=user)
    if current_user.role == Role.ADMIN:
        return redirect(url_for("pages.admin_page"))
    if current_user.role == Role.NURSE:
        return redirect(url_for("pages.health_home_page"))
    return redirect(url_for("pages.doctor_home_page"))


@api.route("/api/password/<user_id>", methods=["POST"])
@login_required
def password_change_api(user_id):
    "password change"
    # pylint: disable=no-member
    pw = request.form.get("password")
    cpw = request.form.get("confirm")
    if pw == cpw:
        db.session.begin()
        user = User.query.filter_by(id=user_id).first()
        user.password = pw
        db.session.commit()
        return redirect(request.referrer)
    flash("Passwords did not match")
    return redirect(request.referrer)


@api.route("/api/user/add", methods=["POST"])
@login_required
def user_add_api():
    "user addition"
    # pylint: disable=no-member
    db.session.begin()
    user = User(
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        email=request.form.get("email"),
        password="".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        role=Role[request.form.get("role").upper()],
    )
    print(user, flush=True)
    db.session.add(user)
    db.session.commit()
    return redirect(request.referrer)


@api.route("/api/patient/add", methods=["POST"])
@login_required
def patient_add_api():
    "patient addition"
    # pylint: disable=no-member
    db.session.begin()
    patient = Patient(
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        email=request.form.get("email"),
        date_of_birth=request.form.get("date_of_birth"),
        insurance_number=request.form.get("insurance_number"),
        govt_id=request.form.get("govt_id"),
    )
    print(patient, flush=True)
    db.session.add(patient)
    db.session.commit()
    return redirect(request.referrer)


@api.route("/api/appt/add", methods=["POST"])
@login_required
def appt_add_api():
    "user addition"
    # pylint: disable=no-member
    db.session.begin()
    appt = Appointment(
        patient_id=request.form.get("patient"),
        doctor_id=request.form.get("doctor"),
        date=request.form.get("date").replace("T", " "),
        emergency=request.form.get("emergency") is not None,
    )
    db.session.add(appt)
    db.session.commit()
    return redirect(request.referrer)

@api.route("/api/report/<appointment_id>", methods=["POST"])
@login_required
def report_api(appointment_id):
    "user addition"
    # pylint: disable=no-member
    db.session.begin()
    print(request.form, appointment_id, flush=True)
    appt = Appointment.query.filter_by(id=appointment_id).first()
    appt.completed = True
    report = Report(
        patient_id=appt.patient.id,
        doctor_id=appt.doctor.id,
        comment=request.form.get("comment"),
        appointment_id=appointment_id
    )
    prescription = Prescription(
        patient_id=appt.patient.id,
        doctor_id=appt.doctor.id,
    )
    for med_ndc in request.form.getlist("medications"):
        med = Medication.query.filter_by(ndc=med_ndc).first()
        prescription.medications.append(med)
    report.prescription = prescription
    db.session.commit()
    return redirect(url_for("pages.doctor_home_page"))


@api.route("/api/logout", methods=["POST"])
@login_required
def logout_api():
    "logout"
    logout_user()
    flash("You have been logged out")
    return redirect("/")
