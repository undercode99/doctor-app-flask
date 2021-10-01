from .controllers.patient import PatientsController, PatientsListController, UpdateVaccinePatientController
from .controllers.employee import EmployeesListController, EmployeesController
from .controllers.doctor import DoctorsListController, DoctorsController
from .controllers.appointment import AppointmentsListController, AppointmentsController
from .controllers.auth import AuthLogin

def initialize_routes(api):
    
    ## auth login
    api.add_resource(AuthLogin, "/login")

    ## employees resource
    api.add_resource(EmployeesListController, '/employees')
    api.add_resource(EmployeesController, '/employees/<int:id>')

    ## Doctor resource
    api.add_resource(DoctorsListController, '/doctors')
    api.add_resource(DoctorsController, '/doctors/<int:id>')


    
    ## patient resource
    api.add_resource(PatientsListController, '/patients')
    api.add_resource(PatientsController, '/patients/<int:id>')
    
    
    ## appointment resource
    api.add_resource(AppointmentsListController, '/appointments')
    api.add_resource(AppointmentsController, '/appointments/<int:id>')


    api.add_resource(UpdateVaccinePatientController, "/patients/update-vaccine")