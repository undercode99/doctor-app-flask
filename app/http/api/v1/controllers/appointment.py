
from app.http.api.v1.validations.appointment import create_appointment_validate, update_appointment_validate,  to_datetime
from app.http.middleware.token_required_jwt import token_required_jwt
from app.http.response import Response
from app.services.exceptions import ExceptionUserNotFound
from app.services.exceptions.appointments import ExceptionAppointmentsHasBooked, ExceptionAppointmentsInvalidTime
from flask_restful import Resource
from app.services import AppointmentsServices
from flask import request
import jwt


class AppointmentsListController(Resource):
    method_decorators   = { 'get': [token_required_jwt], 'post': [token_required_jwt]}
    
    def get(self, user):
        try:
            appointment =  [ doctor.toDict() for doctor in AppointmentsServices.listAppointments() ]
            return Response({'data': appointment}).send()
        except Exception as e:
            return Response().serverError(errorMessage=str(e))

    
   
    def post(self, user):
        try:
            data = request.get_json()

            # response request
            validate = create_appointment_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to create appointment", errorMessage=validate['message'])
           
            data["datetime"] = to_datetime(data["datetime"])

            result = AppointmentsServices.createAppointments(**data)
            return Response({'data': result.toDict()}).created(message="Appointment has been created")

        except (ExceptionAppointmentsInvalidTime, ExceptionAppointmentsHasBooked, ExceptionUserNotFound) as e:
            return Response().badRequest(message="Failed to create appointment", errorMessage=str(e))
        except Exception as e:
            return Response().serverError(message="Failed to create appointment", errorMessage=str(e))


class AppointmentsController(Resource):

    method_decorators   = { 'delete': [token_required_jwt], 'get': [token_required_jwt], 'put': [token_required_jwt]}

    def delete(self, user, id):
        try:
            AppointmentsServices.deleteAppointments(id)
            return Response().send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def get(self, user, id):
        try:
            appointment  = AppointmentsServices.getAppointmentsById(id)
            return Response({'data': appointment.toDict()}).send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))

    
    def put(self, user, id):
        try:
            data = request.get_json()
            # response request
            validate = update_appointment_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to update appointment", errorMessage=validate['message'])

            if "datetime" in  data:
                data["datetime"] = to_datetime(data["datetime"])
            
            data["id"] = id
            result = AppointmentsServices.updateAppointments(**data)
            return Response({'data': result.toDict()}).created(message="Appointment has been updated")

        except (ExceptionAppointmentsInvalidTime, ExceptionAppointmentsHasBooked, ExceptionUserNotFound) as e:
            return Response().badRequest(message="Failed to update appointment", errorMessage=str(e))
        except Exception as e:
            return Response().serverError(message="Failed to update appointment", errorMessage=str(e))

