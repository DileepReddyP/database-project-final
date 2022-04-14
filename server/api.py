import random
import string
from flask import Blueprint, redirect, request, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user

from server.models import User, db, Role

api = Blueprint("api", __name__)

@api.route('/api/login', methods=["POST"])
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
    return redirect(url_for("pages.index"))

@api.route('/api/user/add',  methods=["POST"])
@login_required
def user_add_api():
    "user addition"
    # pylint: disable=no-member
    db.session.begin()
    user = User(
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        email=request.form.get("email"),
        password=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        role=Role[request.form.get("role").upper()]
    )
    print(user, flush=True)
    db.session.add(user)
    db.session.commit()
    return redirect(request.referrer)

@api.route('/api/patient/add',  methods=["POST"])
@login_required
def patient_add_api():
    "patient addition"
    # pylint: disable=no-member
    # db.session.begin()
    # user = User(
    #     first_name=request.form.get("first_name"),
    #     last_name=request.form.get("last_name"),
    #     email=request.form.get("email"),
    #     password=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
    #     role=Role[request.form.get("role").upper()]
    # )
    print(request.form)# user, flush=True)
    # db.session.add(user)
    # db.session.commit()
    return redirect(request.referrer)

@api.route('/api/appt/add',  methods=["POST"])
@login_required
def appt_add_api():
    "user addition"
    # pylint: disable=no-member
    db.session.begin()
    user = User(
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        email=request.form.get("email"),
        password=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        role=Role[request.form.get("role").upper()]
    )
    print(user, flush=True)
    db.session.add(user)
    db.session.commit()
    return redirect(request.referrer)

@api.route('/api/logout',  methods=["POST"])
@login_required
def logout_api():
    "logout"
    logout_user()
    flash("You have been logged out")
    return redirect("/")
