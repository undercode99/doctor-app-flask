from .base import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Doctors(db.Model):

    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender  = db.Column(db.String(100) , nullable=False)
    birthdate  = db.Column(db.DateTime , nullable=False)
    work_start_time = db.Column(db.Time() , nullable=False, doc='naive time')
    work_end_time = db.Column(db.Time() , nullable=False, doc='naive time')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self,name, username, password, gender, birthdate,  work_start_time, work_end_time):
        self.name = name
        self.username = username
        self.password = generate_password_hash(password)
        self.gender = gender
        self.birthdate = birthdate
        self.work_start_time = work_start_time
        self.work_end_time = work_end_time

    
    def passwordIsValid(self, plaintextPassword):
        return check_password_hash(self.password, plaintextPassword)
    
    def updatePassword(self, plaintextPassword):
        self.password = generate_password_hash(plaintextPassword)

    def doctorIsAvailable(self, datetime: datetime):
        if self.work_start_time > datetime.time():
            return False
        if self.work_end_time < datetime.time():
            return False
        return True

    
    def toDict(self, hide_password = True):
        dict_data =  {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "gender": self.gender,
            "birthdate" : self.birthdate.strftime("%Y-%m-%d"),
            "work_start_time": self.work_start_time.strftime("%H:%M"),
            "work_end_time": self.work_end_time.strftime("%H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d"),
            "created_at": self.created_at.strftime("%Y-%m-%d")
        }
        if not hide_password:
            dict_data["password"] = self.password

        return dict_data