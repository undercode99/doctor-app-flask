
from app.repositories import PatientsRepository
from app.repositories.base import ExceptionIntegrityErrorRepository
from app.models import Patients
from .exceptions import ExceptionUserNotFound, ExceptionUserHasRegister
from google.cloud import bigquery
from google.oauth2 import service_account
from flask import current_app

class PatientServices:

    @classmethod
    def listPatients(cls):
        patinents = PatientsRepository(Patients).all()
        return patinents

    
    @classmethod
    def getPatientsById(cls, id: int):
        patient = PatientsRepository(Patients).firstByid(id)
        if patient is None:
            raise ExceptionUserNotFound("Data pasien tidak di temukan")
        return patient

    @classmethod
    def registerPatient(cls, name, gender, birthdate, no_ktp, address) -> Patients:
        data_patient = Patients(
            name=name,
            gender=gender,
            birthdate=birthdate,
            no_ktp=no_ktp,
            address=address
        )

        try:
            save_patient = PatientsRepository(data_patient).createOrUpdate()
            return save_patient
        except ExceptionIntegrityErrorRepository as e:
            raise ExceptionUserHasRegister("No ktp {} sudah terdaftar".format(no_ktp))
        except Exception as e:
            raise Exception(e)


    @classmethod
    def updatePatientById(cls, id: int,  name:str = None, gender:str = None, birthdate:str= None, no_ktp:str= None, address:str= None) -> Patients:
        patient = cls.getPatientsById(id)
        
        if name:
            patient.name = name
        if gender:
            patient.gender = gender
        if birthdate:
            patient.birthdate = birthdate
        if no_ktp:
            patient.no_ktp = no_ktp
        if address:
            patient.address = address

        update_patient = PatientsRepository(patient).createOrUpdate()

        return update_patient

    
    @classmethod
    def updateVaccinePatient(cls, no_ktp: str, vaccine_type: str = None, vaccine_count: str = None):
        patient = PatientsRepository(Patients).firstByNoKTP(no_ktp=no_ktp)
        if patient is None:
            raise ExceptionUserNotFound("Data pasien dengan no ktp {} tidak di temukan".format(no_ktp))
        if vaccine_type:
            patient.vaccine_type = vaccine_type
        if vaccine_count:
            patient.vaccine_count = vaccine_count
        return PatientsRepository(patient).createOrUpdate()


    @classmethod
    def deletePatient(cls, id: int):
        patient = cls.getPatientsById(id)
        PatientsRepository(patient).delete()


    @classmethod
    def updateVaccineFromGoogleBigQuery(cls):
        credentials = service_account.Credentials.from_service_account_file(
           current_app.config["GOOGLE_CLOUD_CREDENTIAL"] , scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        client = bigquery.Client(credentials=credentials)
        # Perform a query.
        QUERY = "SELECT no_ktp, vaccine_type, vaccine_count FROM `delman-interview.interview_mock_data.vaccine-data` limit 5"
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
        results = []
        for row in rows:
            try:
                result = cls.updateVaccinePatient(no_ktp=str(row['no_ktp']), vaccine_count=str(row['vaccine_count']), vaccine_type=str(row['vaccine_type']))
                results.append(result)
            except Exception as e:
                print(e)

        return results