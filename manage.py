"""
manage.py
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""

from flask_migrate import Migrate
from flask.cli import cli

from app.main import create_app
from app.models import db

app = create_app()

migrate = Migrate()
migrate.init_app(app, db)
