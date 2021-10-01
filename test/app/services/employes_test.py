import copy
from app.services import EmployeesService
from app.services.exceptions import ExceptionUserHasRegister, ExceptionUserInvalidPassword, ExceptionUserNotFound
from app.models import Employees
from datetime import date, timedelta
import pytest

def data_register_services(username="employee_test_service"):
    return EmployeesService.registerEmployee(
        name="Employee From Services",
        username=username,
        password="employee_test_service",
        gender="male",
        birthdate=date.today()
    )


def test_register_employee_services(app):
    with app.app_context():
        assert isinstance(data_register_services(), Employees) 


def test_register_duplicate_employee_username_services(app):
    with app.app_context():
        with pytest.raises(ExceptionUserHasRegister):
            data_register_services()


def test_get_id_employee_services(app):
    with app.app_context():
        reg = data_register_services(username="new_employee_sevices")
        employee_by_id = EmployeesService.getEmployeeById(reg.id)
        assert isinstance(employee_by_id, Employees)
        assert reg.id == employee_by_id.id
        assert reg.username == employee_by_id.username

def test_update_employee_services(app):
    with app.app_context():
        reg = data_register_services(username="employee_for_update")
        username = copy.copy(reg.username)
        password = copy.copy(reg.password)
        birthdate = copy.copy(reg.birthdate)
        gender = copy.copy(reg.gender)
        id = copy.copy(reg.id)
        employee_update = EmployeesService.updateEmplpoyee(id=reg.id, username="employee_username_has_update", password="New_Password", gender="female")
        assert employee_update.username != username
        assert employee_update.password != password
        assert employee_update.gender != gender
        assert employee_update.birthdate == birthdate
        assert employee_update.id == id
        
        ## Test login
        EmployeesService.login(username="employee_username_has_update", password="New_Password")

def test_get_all_employee_services(app):
    with app.app_context():
        employee_list = EmployeesService.listEmployee()
        assert len(employee_list) >= 1

        for employe in employee_list:
            assert isinstance(employe, Employees)


def test_login_username_notfound_employee_services(app):
    with app.app_context():
        with pytest.raises(ExceptionUserNotFound):
            EmployeesService.login(username="employee_ngasal", password="employee_test_service")


def test_login_password_invalid_emplyee_services(app):
    with app.app_context():
        with pytest.raises(ExceptionUserInvalidPassword):
            EmployeesService.login(username="employee_test_service", password="password_ngasal")


def test_login_valid_emplyee_services(app):
    with app.app_context():
        employe = EmployeesService.login(username="employee_test_service", password="employee_test_service")
        assert isinstance(employe, Employees)



