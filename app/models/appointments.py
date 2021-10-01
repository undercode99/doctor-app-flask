import enum

from app.models import patients
from .base import db
from sqlalchemy import Enum

class StatusAppointmentEnum(enum.Enum):
    IN_QUEUE = "IN_QUEUE"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

    
    def __init__(self, *args):
        self.values = args
    
    
    def __new__(cls, value, *arg):
        obj = object.__new__(cls)
        obj._value = value
        return obj


class Appointments(db.Model):

    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id  = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient = db.relationship("Patients", backref=db.backref("patients", uselist=False))
    doctor = db.relationship("Doctors", backref=db.backref("doctors", uselist=False))
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum(StatusAppointmentEnum), nullable=False)
    diagnose = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    def toDict(self):
        return {
            "id": self.id,
            "patient": self.patient.toDict(),
            "doctor": self.doctor.toDict(),
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M"),
            "status": self.status.value,
            "diagnose": self.diagnose,
            "notes": self.notes,
            "updated_at": self.updated_at.strftime("%Y-%m-%d"),
            "created_at": self.created_at.strftime("%Y-%m-%d")
        }

