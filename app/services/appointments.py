
from app.models.appointments import StatusAppointmentEnum
from app.repositories import AppointmentsRepository
from app.models import Appointments
from app.services.doctors import DoctorsService
from app.services.exceptions import ExceptionUserNotFound, ExceptionAppointmentsInvalidTime, ExceptionAppointmentsHasBooked
from datetime import date, datetime

from app.services.patients import PatientServices

class AppointmentsServices:

    @classmethod
    def listAppointments(cls) -> list:
        appointments = AppointmentsRepository(Appointments).all()
        return appointments

    
    @classmethod
    def getAppointmentsById(cls, id: int) -> Appointments:
        appointments = AppointmentsRepository(Appointments).firstByid(id)
        if appointments is None:
            raise ExceptionUserNotFound("Data appointments tidak di temukan")
        return appointments

    @classmethod
    def createAppointments(cls, 
        patient_id:int,
        doctor_id:int,
        datetime: datetime,
        status: str,
        diagnose: str = None, 
        notes: str = None
    ) -> Appointments:

        # Get data doctor and patient
        doctor = DoctorsService.getDoctorById(doctor_id)
        patient = PatientServices.getPatientsById(patient_id)

        if not doctor.doctorIsAvailable(datetime):
            raise ExceptionAppointmentsInvalidTime("Waktu yang di pilih tidak termasuk jam kerja doctor yang bersangkutan")

        # check datetime has booked
        if AppointmentsRepository(Appointments).hasBooked(doctor_id=doctor.id,dt_book=datetime):
            raise ExceptionAppointmentsHasBooked(
                "Waktu yang di pilih sudah di booking dan masih dalam antrian"
            )

        data_appointments = Appointments(
            doctor=doctor,
            patient=patient,
            datetime=datetime,
            status=StatusAppointmentEnum(status),
        )

        if diagnose:
            data_appointments.diagnose = diagnose
        if notes:
            data_appointments.notes = notes

        save_appointments = AppointmentsRepository(data_appointments).createOrUpdate()
        return save_appointments

    

    @classmethod
    def updateAppointments(cls, 
        id: int, 
        patient_id:int = None,
        doctor_id:int = None,
        datetime: datetime = None,
        status: str = None,
        diagnose: str = None, 
        notes: str = None
        ) -> Appointments:

        appointment = cls.getAppointmentsById(id)

        if patient_id:
            appointment.patient =  PatientServices.getPatientsById(patient_id)
        if doctor_id:
            appointment.doctor =  DoctorsService.getDoctorById(doctor_id)
        if datetime:
            appointment.datetime = datetime
        if status:
            appointment.status = status
        if diagnose:
            appointment.diagnose = diagnose
        if notes:
            appointment.notes = notes

        doctor =  DoctorsService.getDoctorById(appointment.doctor_id)
        if not doctor.doctorIsAvailable(appointment.datetime):
            raise ExceptionAppointmentsInvalidTime("Waktu yang di pilih tidak termasuk jam kerja doctor yang bersangkutan")

        # check datetime has booked
        if AppointmentsRepository(Appointments).hasBooked(doctor_id=doctor.id,dt_book=appointment.datetime):
            raise ExceptionAppointmentsHasBooked(
                "Waktu yang di pilih sudah di booking pada jam {} dan masih dalam antrian, silahkan jadwalkan booking "\
                "kurang dari 30 minutes pada jadwal yang sudah di booking dan booking "\
                "lebih dari 30 menit dari jadwal yang sudah di booking"
            )

        update_appointment = AppointmentsRepository(appointment).createOrUpdate()
        return update_appointment
        
        
    @classmethod
    def deleteAppointments(cls, id: int) -> Appointments:
        appointment = cls.getAppointmentsById(id)
        AppointmentsRepository(appointment).delete()
        return appointment


