from ..models import db, Employees
from ..repositories import EmployeesRepository
from datetime import date
from flask import current_app as app

@app.cli.command('seed')
def seed_commands():

    """ Delete if exits """
    firstByUsername = EmployeesRepository(Employees).firstByUsername("employee")
    if firstByUsername:
        EmployeesRepository(firstByUsername).delete()

    """Seed default data to database"""
    employe_admin = Employees(name="Employee Admin", username="employee", password="employee123", gender="laki-laki", birthdate=date.today())
    EmployeesRepository(employe_admin).createOrUpdate()