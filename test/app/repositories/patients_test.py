import pytest
from app.models import Patients
from app.repositories import PatientsRepository
from app.repositories.base import ExceptionIntegrityErrorRepository
from datetime import date
import copy

def test_create_patients(app):
    with app.app_context():
        # create new user
        patients = Patients(
            name="Samsul",
            gender="male",
            birthdate=date.today() ,
            no_ktp="12345",
            address="Simpang 3",
            vaccine_type="Astrazeneca",
            vaccine_count="1"
        )
        copy_data = copy.deepcopy(patients)
        save = PatientsRepository(patients).createOrUpdate()
        assert isinstance(save, Patients)

        # Check valid if insert unique no ktp
        with pytest.raises(ExceptionIntegrityErrorRepository):
            PatientsRepository(copy_data).createOrUpdate()

        fetch_data = PatientsRepository(Patients).firstByNoKTP("12345")
        assert fetch_data.id == patients.id


def test_update_patients(app):
    with app.app_context():
        # Try update
        update = PatientsRepository(Patients).firstByNoKTP("12345")
        update.vaccine_type = "Sinovac"
        update.vaccine_count = "1"
        PatientsRepository(update).createOrUpdate()

        # Check updated
        has_update = PatientsRepository(Patients).firstByNoKTP("12345")
        assert has_update.vaccine_type == "Sinovac"
        assert has_update.vaccine_count  == "1"


def test_filter_patients(app):
    with app.app_context():

        first_by_no_ktp = PatientsRepository(Patients).firstByNoKTP("12345")
        assert first_by_no_ktp

        # query first by id
        first_by_id = PatientsRepository(Patients).firstByid(first_by_no_ktp.id)
        assert first_by_id.name == first_by_no_ktp.name

        # Query find by name
        find_by_name = PatientsRepository(Patients).findBy({"name" : first_by_id.name})
        assert len(find_by_name) != 0
        assert find_by_name[0].id == first_by_id.id


def test_delete_patients(app):
    with app.app_context():

        # Delete by ktp
        to_delete_by_ktp = PatientsRepository(Patients).firstByNoKTP("12345")
        PatientsRepository(to_delete_by_ktp).delete()

        # Check ktp has delete
        first_by_ktp = PatientsRepository(Patients).firstByNoKTP("12345")
        assert first_by_ktp is None
