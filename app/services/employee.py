
from app.repositories import EmployeesRepository, employee
from app.repositories.base import ExceptionIntegrityErrorRepository

from app.models import Employees
from .exceptions import ExceptionUserNotFound, ExceptionUserInvalidPassword, ExceptionUserHasRegister
from datetime import date


class EmployeesService:

    @classmethod
    def login(cls, username, password) -> Employees: 
        
        employee = EmployeesRepository(Employees).firstByUsername(username)
        if employee is None:
            raise ExceptionUserNotFound("Username tidak terdaftar")
        
        if employee.passwordIsValid(password) == False:
            raise ExceptionUserInvalidPassword("Password tidak sesuai dengan username")

        return employee

    
    @classmethod
    def listEmployee(cls):
        employees = EmployeesRepository(Employees).all()
        return employees

    
    @classmethod
    def getEmployeeById(cls, id: int):
        employee = EmployeesRepository(Employees).firstByid(id)
        if employee is None:
            raise ExceptionUserNotFound("Data user employee tidak di temukan")
        
        return employee


    @classmethod
    def registerEmployee(cls, name, username, password, gender, birthdate):
        data_employee = Employees(
            name=name,
            username=username,
            password=password,
            gender=gender,
            birthdate=birthdate
        )

        try:
            save_employee = EmployeesRepository(data_employee).createOrUpdate()
            return save_employee
        except ExceptionIntegrityErrorRepository as e:
            raise ExceptionUserHasRegister("Username dengan {} sudah di gunakan user lain".format(username))
        except Exception as e:
            raise Exception(e)


    @classmethod
    def updateEmplpoyee(cls, id: int, name:str = None, username: str = None, password: str = None, gender: str = None, birthdate: date = None) -> Employees:
        employee = cls.getEmployeeById(id)
        if name:
            employee.name = name
        if username:
            employee.username = username
        if password:
            employee.updatePassword(password)
        if gender:
            employee.gender = gender
        if birthdate:
            employee.birthdate = birthdate
        try:
            update_employee = EmployeesRepository(employee).createOrUpdate()
            return update_employee
        except ExceptionIntegrityErrorRepository as e:
            raise ExceptionUserHasRegister("Username dengan {} sudah di gunakan user lain".format(username))
        except Exception as e:
            raise Exception(e)



    @classmethod
    def deleteEmployee(cls, id: int):
        employee = cls.getEmployeeById(id)
        EmployeesRepository(employee).delete()


