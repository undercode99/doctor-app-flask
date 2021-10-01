
from flask import current_app as app
from flask_migrate import Migrate
from .models import db
from datetime import date

""" Init database """
db.init_app(app)

""" Migreate """    
migrate = Migrate()
migrate.init_app(app, db)



