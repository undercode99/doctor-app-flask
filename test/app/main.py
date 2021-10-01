# import pytest
# from app.models import db
# from app.main import create_app
# from flask_migrate import upgrade



# class ConfigTest:
#     """App configuration."""
#     SCHEDULER_API_ENABLED = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite://'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
    


# @pytest.fixture(scope='session')
# def app():
#     app = create_app(config=ConfigTest())
#     with app.app_context():
#         upgrade()
#         yield app
#         db.drop_all()
#         db.engine.execute("DROP TABLE alembic_version")
#     return app