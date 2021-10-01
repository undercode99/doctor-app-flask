
from flask import Flask

from app.http import api
from .config import Config
from .jobs.job import init_jobs

def create_app(app_name='FLASK_API', config=Config()):

    app = Flask(app_name)
    app.config.from_object(config)
    
    """ Initials jobs """
    init_jobs(app)
    with app.app_context():

        """ initial database """
        from .database import intial_database
        intial_database(app)

        """ initial routes api """
        from .http import register_api
        register_api(app)

        """ Register commands """
        from . import commands


    return app
