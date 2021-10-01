from flask import current_app as app
from flask_cors import CORS
from .v1 import api_v1


""""
  CORS application for api endpoint
  with orgin any
"""
CORS(app, resources={r"/api/*": {"origins": "*"}})


""" 
  Register api blueprint with api version prefix
"""
app.register_blueprint(api_v1, url_prefix="/api/v1")
