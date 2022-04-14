from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy(session_options={"autocommit": True})  # prevents pool overflow


class Role(Enum):
    "role enum"
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"


class User(UserMixin, db.Model):
    "user model with flask-login mixin added"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.Enum(Role))

    def __repr__(self) -> str:
        return f"name: {self.first_name}"


class Patient(db.Model):
    "patient model"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    insurance_number = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime)
    govt_id = db.Column(db.String(50))
    email = db.Column(db.String(100))


class Appointment(db.Model):
    "appointment model"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    patient = db.relationship("Patient", backref=db.backref("appointments"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor = db.relationship("User", backref=db.backref("appointments"))
    date = db.Column(db.DateTime)
    emergency = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)


class Report(db.Model):
    "report model"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    patient = db.relationship("Patient", backref=db.backref("reports"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor = db.relationship("User", backref=db.backref("reports"))
    appointment_id = db.Column(
        db.Integer, db.ForeignKey("appointment.id"), nullable=False
    )
    appointment = db.relationship("Appointment", backref=db.backref("report"))
    comment = db.Column(db.String(2048))
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescription.id"))
    prescription = db.relationship("Prescription", backref=db.backref("report"))


class TestType(Enum):
    "test type enum"
    CONSULTING_ROOM = "consulting room"
    LABORATORY = "laboratory"
    RADIOLOGY = "radiology"


# class Test(db.Model):
#     "test model"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     role = db.Column(db.Enum(TestType))


# class TestReport(db.Model):
#     "test report model"
#     id = db.Column(db.Integer, primary_key=True)
#     test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)
#     test = db.relationship("Test", backref=db.backref("test_reports"))
#     patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
#     patient = db.relationship("Patient", backref=db.backref("test_reports"))
#     comment = db.Column(db.String(2048))
#     date = db.Column(db.DateTime)

med_pres = db.Table(
    "med_pres",
    db.Column("medication_ndc", db.String(20), db.ForeignKey("medication.ndc")),
    db.Column("prescription_id", db.Integer, db.ForeignKey("prescription.id")),
)


class Medication(db.Model):
    "Medications Model"
    ndc = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))


class Prescription(db.Model):
    "prescription model"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    patient = db.relationship("Patient", backref=db.backref("prescriptions"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    doctor = db.relationship("User", backref=db.backref("prescriptions"))
    medications = db.relationship(
        "Medication", secondary=med_pres, backref="prescriptions"
    )
