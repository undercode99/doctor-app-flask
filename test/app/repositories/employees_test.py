import pytest
from app.models import Employees
from app.repositories import EmployeesRepository
from app.repositories.base import ExceptionIntegrityErrorRepository
from datetime import date
import copy


def test_create_employees(app):
    with app.app_context():

        # create new user
        data = Employees(name="Employee User", username="employee", password="employee123", birthdate=date.today(), gender="male")
        copy_data = copy.deepcopy(data)
        save = EmployeesRepository(data).createOrUpdate()
        assert isinstance(save, Employees) 

        # Check valid if insert unique username
        with pytest.raises(ExceptionIntegrityErrorRepository):
            EmployeesRepository(copy_data).createOrUpdate()

        fetch_data = EmployeesRepository(Employees).firstBy({"username": "employee"})
        assert fetch_data.id == data.id


def test_update_employees(app):
    with app.app_context():

        # Try update
        update = EmployeesRepository(Employees).firstByUsername("employee")
        update.gender = "female"
        update.name = "Employee Super User"
        update.birthdate = date(2020, 10, 24)
        EmployeesRepository(update).createOrUpdate()

        # Check updated
        has_update = EmployeesRepository(Employees).firstByUsername("employee")
        assert has_update.gender == "female"
        assert has_update.name  == "Employee Super User"
        assert has_update.birthdate.year == 2020
        assert has_update.birthdate.month == 10
        assert has_update.birthdate.day == 24


def test_filter_employees(app):
    with app.app_context():

        first_by_username = EmployeesRepository(Employees).firstByUsername("employee")
        assert first_by_username

        # query first by id
        first_by_id = EmployeesRepository(Employees).firstByid(first_by_username.id)
        assert first_by_id.username == first_by_username.username

        # Query find by name
        find_by_name = EmployeesRepository(Employees).findBy({"name":first_by_id.name})
        assert len(find_by_name) != 0
        assert find_by_name[0].id == first_by_id.id


def test_password_employees():
    first_by_username = EmployeesRepository(Employees).firstByUsername("employee")
    assert first_by_username.passwordIsValid("employee123")


def test_delete_employees():

    # Delete by username
    to_delete_by_username = EmployeesRepository(Employees).firstByUsername("employee")
    EmployeesRepository(to_delete_by_username).delete()

    # Check username has delete
    first_by_username = EmployeesRepository(Employees).firstByUsername("employee")
    assert first_by_username is None
