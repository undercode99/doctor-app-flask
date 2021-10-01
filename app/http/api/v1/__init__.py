from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

api_v1 = Blueprint('api_v1', __name__)

# RESFUL API
resful_api = Api(api_v1)
initialize_routes(resful_api)