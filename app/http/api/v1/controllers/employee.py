from datetime import date
from app.http.api.v1.validations.employee import create_employee_validate, to_date, update_employee_validate
from app.http.middleware.token_required_jwt import token_required_jwt
from app.http.response import Response
from app.services.exceptions.base import ExceptionUserHasRegister, ExceptionUserNotFound
from flask_restful import Resource
from app.services import EmployeesService
from flask import request



class EmployeesListController(Resource):
    method_decorators   = { 'get': [token_required_jwt], 'post': [token_required_jwt]}
    
    def get(self, user):
        try:
            employees =  [ employe.toDict() for employe in EmployeesService.listEmployee()]
            return Response({'data': employees}).send()
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def post(self, user):
        try:
            data = request.get_json()
            # response request
            validate = create_employee_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to register employee", errorMessage=validate['message'])
           
            data["birthdate"] = to_date(data["birthdate"])
            result = EmployeesService.registerEmployee(**data)
            return Response({'data': result.toDict()}).created(message="Employee has been registered")

        except ExceptionUserHasRegister as e:
            return Response().badRequest(message="Failed to register employee", errorMessage=str(e))

        except Exception as e:
            return Response().serverError(message="Failed to register employee", errorMessage=str(e))



class EmployeesController(Resource):
    method_decorators   = { 'delete': [token_required_jwt], 'get': [token_required_jwt], 'put': [token_required_jwt]}

    def delete(self, user, id):
        try:
            EmployeesService.deleteEmployee(id)
            return Response().send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))


    def get(self, user, id):
        try:
            employee  = EmployeesService.getEmployeeById(id)
            return Response({'data': employee.toDict()}).send()
        except ExceptionUserNotFound as e:
            return Response().notfound(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))

    
    def put(self, user, id):
        try:
            data = request.get_json()
            # response request
            validate = update_employee_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed to update employee", errorMessage=validate['message'])
            if "birthdate" in  data:
                data["birthdate"] = to_date(data["birthdate"])
            
            data["id"] = id
            result = EmployeesService.updateEmplpoyee(**data)
            return Response({'data': result.toDict()}).created(message="Employee has been updated")

        except ExceptionUserHasRegister as e:
            return Response().badRequest(message="Failed to update employee", errorMessage=str(e))

        except Exception as e:
            return Response().serverError(message="Failed to update employee", errorMessage=str(e))

