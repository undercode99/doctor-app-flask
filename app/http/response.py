from flask import jsonify, current_app
import traceback

class Response:

    response = {
        "error": False,
        "message": "Success",
        "responseCode": 200,
        "errorMessage": None,
        # "traceBack": None
    }

    def __init__(self, data={}):
        self.response = {**self.response, **data}

    def send(self, **data):
        # self.response['traceBack'] = str(traceback.format_exc())
        self.response = {**self.response, **data}
        # if current_app.config['DEBUG'] == False or self.response['error'] == False:
        #     self.response.pop("traceBack")
        return self.response, self.response['responseCode']

    def sendError(self, message, errorMessage, code):
        responseError = {
            "message": message,
            "errorMessage": errorMessage,
            "error": True,
            "responseCode": code
        }
        self.response = {**self.response, **responseError}
        return self.send()
    
        
    def badRequest(self, message="Bad Request", errorMessage=""):
        return self.sendError(message, errorMessage,code=400)
    
    
    def serverError(self, message="Internal Server Error", errorMessage=None):
        return self.sendError(message, errorMessage,code=500)
    
    def unauthorized(self, message="Opps! Invalid credentials", errorMessage=None):
        return self.sendError(message, errorMessage,code=401)
    
    def forbidden(self, message="Access forbbiden", errorMessage="Access forbbiden"):
        return self.sendError(message, errorMessage,code=403)

    def notfound(self, message="Not found", errorMessage="Not found"):
        return self.sendError(message, errorMessage, code=404)

    def created(self, message="Data has been created"):
        created = {
            'message': message,
            'responseCode': 201
        }
        self.response = {**self.response, **created}
        return self.send()
