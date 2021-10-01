
from app.repositories import DoctorsRepository
from app.repositories.base import ExceptionIntegrityErrorRepository

from app.models import Doctors, doctors
from .exceptions import ExceptionUserHasRegister, ExceptionUserNotFound, ExceptionDoctorFailedWorkTime
from datetime import time, date

class DoctorsService:

    @classmethod
    def listDoctor(cls) -> list:
        doctors = DoctorsRepository(Doctors).all()
        return doctors

    
    @classmethod
    def getDoctorById(cls, id: int) -> Doctors:
        doctor = DoctorsRepository(Doctors).firstByid(id)
        if doctor is None:
            raise ExceptionUserNotFound("Data user dokter tidak di temukan")
        
        return doctor


    @classmethod
    def registerDoctor(cls, name:str, username:str, password:str, gender:str, birthdate:date, work_start_time:time, work_end_time:time) -> Doctors:
        data_doctor = Doctors(
            name=name,
            username=username,
            password=password,
            gender=gender,
            birthdate=birthdate,
            work_start_time = work_start_time,
            work_end_time = work_end_time
        )
        
        if data_doctor.work_start_time >= data_doctor.work_end_time:
            raise ExceptionDoctorFailedWorkTime("Akhir jam kerja dokter harus lebih tinggi dari start jam kerjanya")
            

        try:
            save_doctor = DoctorsRepository(data_doctor).createOrUpdate()
            return save_doctor
        except ExceptionIntegrityErrorRepository as e:
            raise ExceptionUserHasRegister("Username dengan {} sudah di gunakan user dokter lain".format(username))
        except Exception as e:
            raise Exception(e)
    
    
    @classmethod
    def updateDoctor(cls, 
        id: int,
        username: str = None,
        password: str = None,
        gender: str = None,
        birthdate: date = None,
        work_start_time:time = None,
        work_end_time:time = None
    ) -> Doctors:

        doctor = cls.getDoctorById(id)
        if username:
            doctor.username = username
        if password:
            doctor.updatePassword(password)
        if gender:
            doctor.gender = gender
        if birthdate:
            doctor.birthdate = birthdate
        if work_start_time:
            doctor.work_start_time = work_start_time
        if work_end_time:
            doctor.work_end_time = work_end_time

        if doctor.work_start_time >= doctor.work_end_time:
            raise ExceptionDoctorFailedWorkTime("Akhir jam kerja dokter harus lebih tinggi dari start jam kerjanya")
            
        return DoctorsRepository(doctor).createOrUpdate()



    @classmethod
    def deleteDoctor(cls, id: int) -> Doctors:
        doctor = cls.getDoctorById(id)
        DoctorsRepository(doctor).delete()
        return doctor


