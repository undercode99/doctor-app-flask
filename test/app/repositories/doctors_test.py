import pytest
from app.models import Doctors
from app.repositories import DoctorsRepository
from app.repositories.base import ExceptionIntegrityErrorRepository
from datetime import date,datetime, timedelta, time
import copy

def test_create_doctors(app):
    with app.app_context():

        # create new user
        data = Doctors(
            name="Doctor Amanda",
            username="amanda98",
            password="doctorAmandMantaps",
            birthdate=date.today() ,
            gender="female",
            work_start_time=time(8, 0),
            work_end_time=time(16, 0)
        )
        copy_data = copy.deepcopy(data)
        save = DoctorsRepository(data).createOrUpdate()
        assert isinstance(save, Doctors) 

        # Check valid if insert unique username
        with pytest.raises(ExceptionIntegrityErrorRepository):
            DoctorsRepository(copy_data).createOrUpdate()

        fetch_data = DoctorsRepository(Doctors).firstBy({"username": "amanda98"})
        assert fetch_data.id == data.id


def test_update_doctors(app):
    with app.app_context():
        

        # Try update
        update = DoctorsRepository(Doctors).firstByUsername("amanda98")
        update.gender = "male"
        update.name = "dr. Doctor Super User"
        end_time = time(15, 0)
        update.work_end_time = end_time
        DoctorsRepository(update).createOrUpdate()

        # Check updated
        has_update = DoctorsRepository(Doctors).firstByUsername("amanda98")
        assert has_update.gender == "male"
        assert has_update.name  == "dr. Doctor Super User"
        assert has_update.work_end_time == end_time


def test_filter_doctors(app):
    with app.app_context():

        first_by_username = DoctorsRepository(Doctors).firstByUsername("amanda98")
        assert first_by_username

        # query first by id
        first_by_id = DoctorsRepository(Doctors).firstByid(first_by_username.id)
        assert first_by_id.username == first_by_username.username

        # Query find by name
        find_by_name = DoctorsRepository(Doctors).findBy({"name" : first_by_id.name})
        assert len(find_by_name) != 0
        assert find_by_name[0].id == first_by_id.id


def test_password_valid_doctors(app):
    with app.app_context():
        first_by_username = DoctorsRepository(Doctors).firstByUsername("amanda98")
        assert first_by_username.passwordIsValid("doctorAmandMantaps")


def test_delete_doctors(app):
    with app.app_context():

        # Delete by username
        to_delete_by_username = DoctorsRepository(Doctors).firstByUsername("amanda98")
        DoctorsRepository(to_delete_by_username).delete()

        # Check username has delete
        first_by_username = DoctorsRepository(Doctors).firstByUsername("amanda98")
        assert first_by_username is None
