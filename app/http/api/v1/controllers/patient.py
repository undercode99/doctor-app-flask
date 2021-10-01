from datetime import date
from app.http.api.v1.validations.patient import create_patient_validate, to_date, update_patient_validate
from app.http.middleware.token_required_jwt import token_required_jwt
from app.http.response import Response
from app.services.exceptions.base import ExceptionUserHasRegister, ExceptionUserNotFound
from flask_restful import Resource
from app.services import PatientServices
from flask import request



class PatientsListController(Resource):
    method_decorators   = { 'get': [token_required_jwt], 'post': [token_required_jwt]}
    
    def get(self, user):
        try:
            patients =  [ patient.toDict() for patient in PatientServices.listPatients()]
            return Response({'data': patients}).send()
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def post(self, user):
        try:
            data = request.get_json()
            # response request
            validate = create_patient_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to register patient", errorMessage=validate['message'])
           
            data["birthdate"] = to_date(data["birthdate"])
            result = PatientServices.registerPatient(**data)
            return Response({'data': result.toDict()}).created(message="Patient has been registered")

        except ExceptionUserHasRegister as e:
            return Response().badRequest(message="Failed to register patient", errorMessage=str(e))

        except Exception as e:
            return Response().serverError(message="Failed to register patient", errorMessage=str(e))



class PatientsController(Resource):
    method_decorators   = { 'delete': [token_required_jwt], 'get': [token_required_jwt],  'put': [token_required_jwt]}

    def delete(self, user, id):
        try:
            PatientServices.deletePatient(id)
            return Response().send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def get(self, user, id):
        try:
            patient  = PatientServices.getPatientsById(id)
            return Response({'data': patient.toDict()}).send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))

    def put(self, user, id):
        try:
            data = request.get_json()
            # response request
            validate = update_patient_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to update patient", errorMessage=validate['message'])
            if 'birthdate' in data:
                data["birthdate"] = to_date(data["birthdate"])
            data["id"] = id
            result = PatientServices.updatePatientById(**data)
            return Response({'data': result.toDict()}).created(message="Patient has been updated")

        except ExceptionUserHasRegister as e:
            return Response().badRequest(message="Failed to update patient", errorMessage=str(e))

        except Exception as e:
            return Response().serverError(message="Failed to update patient", errorMessage=str(e))




class UpdateVaccinePatientController(Resource):
    method_decorators   = {'get': [token_required_jwt]}
    def get(self, user):
        try:
            patient_updated = [patient.toDict() for patient in PatientServices.updateVaccineFromGoogleBigQuery()]
            return Response({'data': patient_updated, "message": "Result data patient vaccine has updated"}).send()
        except Exception as e:
            return Response().serverError(errorMessage=str(e))
