from datetime import date
from app.http.api.v1.validations.doctor import create_doctor_validate, to_date, update_doctor_validate,  to_time_hours
from app.http.middleware.token_required_jwt import token_required_jwt
from app.http.response import Response
from app.services.exceptions.base import ExceptionUserHasRegister, ExceptionUserNotFound
from flask_restful import Resource
from app.services import DoctorsService
from flask import request



class DoctorsListController(Resource):
    method_decorators   = { 'get': [token_required_jwt], 'post': [token_required_jwt]}
    
    def get(self, user):
        try:
            doctors =  [ doctor.toDict() for doctor in DoctorsService.listDoctor()]
            return Response({'data': doctors}).send()
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def post(self, user):
        try:
            data = request.get_json()
            # response request
            validate = create_doctor_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to register doctor", errorMessage=validate['message'])
           
            data["birthdate"] = to_date(data["birthdate"])
            data["work_start_time"] = to_time_hours(data["work_start_time"]).time()
            data["work_end_time"] = to_time_hours(data["work_end_time"]).time()
            result = DoctorsService.registerDoctor(**data)
            return Response({'data': result.toDict()}).created(message="Doctor has been registered")

        except ExceptionUserHasRegister as e:
            return Response().badRequest(message="Failed to register doctor", errorMessage=str(e))

        except Exception as e:
            return Response().serverError(message="Failed to register doctor", errorMessage=str(e))



class DoctorsController(Resource):
    method_decorators   = { 'delete': [token_required_jwt], 'get': [token_required_jwt], 'put': [token_required_jwt]}

    def delete(self, user, id):
        try:
            DoctorsService.deleteDoctor(id)
            return Response().send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def get(self, user, id):
        try:
            doctor  = DoctorsService.getDoctorById(id)
            return Response({'data': doctor.toDict()}).send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def put(self, user, id):
        try:
            data = request.get_json()
            # response request
            validate = update_doctor_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to update doctor", errorMessage=validate['message'])
           

            if "birthdate" in data:
                data["birthdate"] = to_date(data["birthdate"])
            if "work_start_time" in data:
                data["work_start_time"] = to_time_hours(data["work_start_time"]).time()
            if "work_end_time" in data:
                data["work_end_time"] = to_time_hours(data["work_end_time"]).time()
                
            data["id"] = id
            result = DoctorsService.updateDoctor(**data)
            return Response({'data': result.toDict()}).created(message="Doctor has been updated")

        except ExceptionUserHasRegister as e:
            return Response().badRequest(message="Failed to update doctor", errorMessage=str(e))

        except Exception as e:
            return Response().serverError(message="Failed to update doctor", errorMessage=str(e))