import copy
from app.models import Patients
from app.services import PatientServices
from app.services.exceptions import ExceptionUserHasRegister, ExceptionUserNotFound
from datetime import date, time
import pytest

def data_register_patient_services(no_ktp="88888888"):
    return PatientServices.registerPatient(
        name="Bambang",
        gender="male",
        birthdate=date.today(),
        no_ktp=no_ktp,
        address="Simpang 9"
    ) 

def test_register_patient_services(app):
    with app.app_context():
        assert isinstance(data_register_patient_services(), Patients) 


def test_register_duplicate_patient_no_ktp_services(app):
    with app.app_context():
        with pytest.raises(ExceptionUserHasRegister):
            data_register_patient_services()


def test_patient_not_found(app):
    with app.app_context():
        with pytest.raises(ExceptionUserNotFound):
            PatientServices.getPatientsById(100000)

def test_get_id_patient_services(app):
    with app.app_context():
        reg = data_register_patient_services(no_ktp="19821928912")
        patient_by_id = PatientServices.getPatientsById(reg.id)
        assert isinstance(patient_by_id, Patients)
        assert reg.id == patient_by_id.id
        assert reg.no_ktp == patient_by_id.no_ktp
        assert reg.name == patient_by_id.name
        assert reg.gender == patient_by_id.gender
        assert reg.birthdate == patient_by_id.birthdate

def test_update_patient_services(app):
    with app.app_context():
        reg = data_register_patient_services(no_ktp="324565643")
        id = copy.copy(reg.id)
        name = copy.copy(reg.name)
        no_ktp = copy.copy(reg.no_ktp)
        patient_update = PatientServices.updatePatientById(id=reg.id, no_ktp="12222", name="Simpleman")
        assert patient_update.name != name
        assert patient_update.no_ktp != no_ktp
        assert patient_update.id == id

def test_update_vaccine_patient(app):
    with app.app_context():
        data_register_patient_services(no_ktp="99999")
        update_vaccine = PatientServices.updateVaccinePatient(no_ktp="99999", vaccine_count="2", vaccine_type="Astrazeneca")

        has_update = PatientServices.getPatientsById(update_vaccine.id)
        assert has_update.vaccine_count == "2"
        assert has_update.vaccine_type == "Astrazeneca"


        update_vaccine_type = PatientServices.updateVaccinePatient(no_ktp="99999", vaccine_type="sinovac")
        has_update_type = PatientServices.getPatientsById(update_vaccine_type.id)
        assert has_update_type.vaccine_type == "sinovac"

        update_vaccine_count = PatientServices.updateVaccinePatient(no_ktp="99999", vaccine_count="1")
        has_update_count = PatientServices.getPatientsById(update_vaccine_count.id)
        assert has_update_count.vaccine_count == "1"
        

def test_get_all_patients_services(app):
    with app.app_context():
        patients_list = PatientServices.listPatients()
        assert len(patients_list) >= 1

        for patient in patients_list:
            assert isinstance(patient, Patients)

