
from flask import Flask
from .config import Config
from .jobs.job import init_jobs

def create_app(app_name='FLASK_API', config=Config()):

    app = Flask(app_name)
    app.config.from_object(config)
    
    """ Initials jobs """
    init_jobs(app)
    with app.app_context():

        """ initial database """
        from . import database

        """ initial routes api """
        from . import http

        """ Register commands """
        from . import commands


    return app
