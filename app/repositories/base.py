from sqlalchemy import exc
from ..models import db, exc

class ExceptionIntegrityErrorRepository(Exception):
    pass

class BaseRepository:

    def __init__(self, model):
        self.model = model

    def firstByid(self, id: int):
        return self.model.query.filter_by(id=id).first()

    def findById(self, id: int):
        return self.model.query.filter_by(id=id).all()

    def all(self):
        return self.model.query.all()

    def firstBy(self, where: dict):
        return self.model.query.filter_by(**where).first()

    def findBy(self, where):
        return self.model.query.filter_by(**where).all()

    def getOrderById(self):
        return self.model.order_by(self.model.id.desc()).all()

    def createOrUpdate(self):
        try:
            db.session.add(self.model)
            db.session.commit()
            return self.model
        except exc.IntegrityError as e:
            db.session.rollback()
            raise ExceptionIntegrityErrorRepository(e)
        except Exception as e:
            db.session.rollback()
            raise ValueError(e)

    def delete(self):
        try:
            db.session.delete(self.model)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(e)

    




