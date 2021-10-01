from app.services import PatientServices
from app.services.appointments import AppointmentsServices
from app.services.doctors import DoctorsService
from datetime import date, datetime, time
import pytest


def test_create_appointment_services(app):
    with app.app_context():
        doctor =  DoctorsService.registerDoctor(
            name="Dr. Mantaps simpleman",
            username="simpledoctor",
            password="doctor_test_service",
            gender="male",
            birthdate=date.today(),
            work_end_time=time(17, 0),
            work_start_time=time(9, 0)
        )

        patient =  PatientServices.registerPatient(
                name="Bambang1",
                gender="male",
                birthdate=date.today(),
                no_ktp="999999881",
                address="Simpang 9"
            ) 


        strg = "2021-09-20 10:00"
        dt = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        AppointmentsServices.createAppointments(
            patient_id=patient.id,
            doctor_id=doctor.id,
            datetime=dt,
            status="IN_QUEUE"
            )

        
        strg = "2021-09-20 13:00"
        dt = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        AppointmentsServices.createAppointments(
            patient_id=patient.id,
            doctor_id=doctor.id,
            datetime=dt,
            status="IN_QUEUE"
            )
        
