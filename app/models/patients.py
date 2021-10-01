from .base import db

class Patients(db.Model):

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255),  nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    no_ktp = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    vaccine_type  = db.Column(db.String(255), nullable=True)
    vaccine_count   = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    def toDict(self):
        dict_data =  {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birthdate" : self.birthdate.strftime("%Y-%m-%d"),
            "no_ktp" : self.no_ktp,
            "address" : self.address,
            "vaccine_type" : self.vaccine_type,
            "vaccine_count" : self.vaccine_count,
            "updated_at": self.updated_at.strftime("%Y-%m-%d"),
            "created_at": self.created_at.strftime("%Y-%m-%d")
        }

        return dict_data