
from datetime import datetime, timedelta
from flask.globals import current_app
from app.http.api.v1.validations.auth import auth_login_validate
from app.http.response import Response
from app.services.exceptions import ExceptionUserNotFound, ExceptionEmployeeInvalidPassword
from flask_restful import Resource
from app.services import EmployeesService
from flask import request
import jwt


class AuthLogin(Resource):
    
    def post(self):
        try:
            data = request.get_json()
            validate = auth_login_validate(data)
            if(validate['isError']):
                return Response().badRequest(message="Failed login", errorMessage=validate['message'])
            
            results = EmployeesService.login(username=data['username'], password=data['password'])
            token = jwt.encode({
                    'sub': results.id,
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(hours=24)
                },
                current_app.config['SECRET_KEY']
            )
            return Response({'data': results.toDict(), 'token': token}).send()
        except ExceptionUserNotFound as e:
            return Response().unauthorized(errorMessage=str(e))
        except ExceptionEmployeeInvalidPassword as e:
            return Response().unauthorized(errorMessage=str(e))
        except Exception as e:
            return Response().serverError(errorMessage=str(e))
