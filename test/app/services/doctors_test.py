import copy
from app.models.doctors import Doctors
from app.services import DoctorsService
from app.services.exceptions import ExceptionUserHasRegister, ExceptionDoctorFailedWorkTime, ExceptionUserNotFound
from datetime import date, time
import pytest

def data_register_doctor_services(username="doctor_test_register",  work_start_time=time(9, 0),  work_end_time=time(17, 0)):
    return DoctorsService.registerDoctor(
        name="Dr. Supratman",
        username=username,
        password="doctor_test_service",
        gender="male",
        birthdate=date.today(),
        work_end_time=work_end_time,
        work_start_time=work_start_time
    )

def test_failed_work_time_doctor(app):
    with app.app_context():

        # same time
        with pytest.raises(ExceptionDoctorFailedWorkTime):
            data_register_doctor_services(work_start_time=time(10, 0), work_end_time=time(10, 0))

        # start gt then end time
        with pytest.raises(ExceptionDoctorFailedWorkTime):
            data_register_doctor_services(work_start_time=time(12, 0), work_end_time=time(10, 0))


def test_register_doctor_services(app):
    with app.app_context():
        assert isinstance(data_register_doctor_services(), Doctors) 


def test_register_duplicate_doctor_username_services(app):
    with app.app_context():
        with pytest.raises(ExceptionUserHasRegister):
            data_register_doctor_services()


def test_doctor_not_found(app):
    with app.app_context():
        with pytest.raises(ExceptionUserNotFound):
            DoctorsService.getDoctorById(100000)

def test_get_id_doctor_services(app):
    with app.app_context():
        reg = data_register_doctor_services(username="new_doctor_test_register")
        doctor_by_id = DoctorsService.getDoctorById(reg.id)
        assert isinstance(doctor_by_id, Doctors)
        assert reg.id == doctor_by_id.id
        assert reg.username == doctor_by_id.username

def test_update_doctor_services(app):
    with app.app_context():
        reg = data_register_doctor_services(username="doctor_for_update")
        id = copy.copy(reg.id)
        username = copy.copy(reg.username)
        password = copy.copy(reg.password)
        work_end_time = copy.copy(reg.work_end_time)
        doctor_update = DoctorsService.updateDoctor(id=reg.id, username="doctor_for_has_update", password="New_Password", work_end_time=time(15, 0))
        assert doctor_update.username != username
        assert doctor_update.password != password
        assert doctor_update.work_end_time != work_end_time
        assert doctor_update.id == id
        

def test_get_all_doctor_services(app):
    with app.app_context():
        doctors_list = DoctorsService.listDoctor()
        assert len(doctors_list) >= 1

        for doctor in doctors_list:
            assert isinstance(doctor, Doctors)

