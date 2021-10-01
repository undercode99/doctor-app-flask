from app.services.employee import EmployeesService
import jwt
from functools import wraps
from flask import request, current_app
from app.http.response import Response

def token_required_jwt(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        error_response = {
            'authenticated': False,
            'error': True,
            'responseCode' : 401
        }
        
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            **error_response
        }

        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            **error_response
        }

        try:
            auth_headers = request.headers.get('Authorization').split()
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms=["HS256"])
            employee = EmployeesService.getEmployeeById(data['sub'])
            return f(employee, *args, **kwargs)

        except jwt.ExpiredSignatureError as e:
            expired_msg['errorMessage'] = str(e)
            return Response(expired_msg).send()

        except jwt.InvalidTokenError as e:
            invalid_msg['errorMessage'] = str(e)
            return Response(invalid_msg).send()

        except Exception as e:
           invalid_msg['errorMessage'] = str(e)
           return Response(invalid_msg).send()

    return _verify
