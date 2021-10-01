from app.repositories.appointments import AppointmentsRepository
from app.models import Doctors, Patients, Appointments, StatusAppointmentEnum, patients
from app.repositories import DoctorsRepository, PatientsRepository
from datetime import date,datetime, time, timedelta
import copy

from app.services.doctors import DoctorsService

def test_appointments(app):
    with app.app_context():

        # Test create 
        doctors = Doctors(
            name="Doctor Sinta",
            username="drsintain",
            password="DoctorSintaCantik",
            birthdate=date.today() ,
            gender="female",
            work_start_time=time(8, 0),
            work_end_time=time(16, 0)
        )

        doctors2 = copy.deepcopy(doctors)
        doctors2.name = "Dockter Endang"
        doctors2.username = "endang123"
        doctors2.password = "endang123"

        DoctorsRepository(doctors).createOrUpdate()

        patients = Patients(
            name="Saefudin",
            gender="male",
            birthdate=date.today() ,
            no_ktp="765678",
            address="Simpang 31",
            vaccine_type="Astrazeneca",
            vaccine_count="1"
        )
        PatientsRepository(patients).createOrUpdate()

        strg = "2021-09-20 10:00"
        dt = datetime.strptime(strg, '%Y-%m-%d %H:%M')

        appointments = Appointments(
            doctor_id=doctors.id,
            patient_id=patients.id,
            datetime=dt,
            status= StatusAppointmentEnum.IN_QUEUE,
            diagnose="Filex",
            notes="Not have money"
        )

        save = AppointmentsRepository(appointments).createOrUpdate()
        assert isinstance(save, Appointments)

        select_appointments = AppointmentsRepository(Appointments).firstByid(appointments.id)
        assert select_appointments.doctor.id == doctors.id
        assert select_appointments.doctor.name == doctors.name
        assert select_appointments.patient.id == patients.id
        assert select_appointments.patient.name == patients.name
        assert select_appointments.patient.no_ktp == patients.no_ktp


        # Test update 
        select_appointments.doctor = doctors2
        AppointmentsRepository(select_appointments).createOrUpdate()
        select_appointments2 = AppointmentsRepository(Appointments).firstByid(appointments.id)
        assert select_appointments2.doctor.id == doctors2.id


        # Test delete 
        select_appointments3 = AppointmentsRepository(Appointments).firstByid(appointments.id)
        AppointmentsRepository(select_appointments3).delete()
        assert AppointmentsRepository(Appointments).firstByid(appointments.id) is None



def get_doctor_by_username(username) -> Doctors:
    return DoctorsRepository(Doctors).firstByUsername(username)


def test_appointments_doctor_is_available(app):
    with app.app_context():

        # Test create 
        doctors = get_doctor_by_username(username="drsintain")

        strg = "2021-09-20 10:30"
        dt = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        assert doctors.doctorIsAvailable(datetime=dt)


def test_appointments_doctor_not_available(app):
    with app.app_context():

        # Test create 
        doctors = get_doctor_by_username(username="drsintain")

        strg = "2021-09-20 07:30"
        dt = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        assert not doctors.doctorIsAvailable(datetime=dt)

        
        strg = "2021-09-20 17:00"
        dt = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        assert not doctors.doctorIsAvailable(datetime=dt)


def test_appointments_has_booked(app):
    with app.app_context():

        # get doctor has booked 
        doctors = get_doctor_by_username(username="drsintain")

        # create new patient
        patients = Patients(
            name="Dirman",
            gender="male",
            birthdate=date.today() ,
            no_ktp="88177",
            address="Simpang 31",
            vaccine_type="Astrazeneca",
            vaccine_count="1"
        )
        PatientsRepository(patients).createOrUpdate()

        

        strg = "2021-09-20 13:00"
        dt_book = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        # Create booked
        appointments = Appointments(
            doctor_id=doctors.id,
            patient_id=patients.id,
            datetime=dt_book,
            status= StatusAppointmentEnum.IN_QUEUE,
        )

        AppointmentsRepository(appointments).createOrUpdate()
        
        strg = "2021-09-20 12:30"
        dt_book = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        assert AppointmentsRepository(Appointments).hasBooked(doctor_id=doctors.id,dt_book=dt_book)

        strg = "2021-09-20 13:40"
        dt_book = datetime.strptime(strg, '%Y-%m-%d %H:%M')
        assert not AppointmentsRepository(Appointments).hasBooked(doctor_id=doctors.id,dt_book=dt_book)

