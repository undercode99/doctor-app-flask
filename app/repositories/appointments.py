from app.models.appointments import StatusAppointmentEnum
from .base import BaseRepository
from datetime import datetime, timedelta

class AppointmentsRepository(BaseRepository):

    def hasBooked(self, doctor_id: int,  dt_book: datetime):
        return self.model.query.filter(
            dt_book - timedelta(minutes=30) <= self.model.datetime, 
            dt_book + timedelta(minutes=30) >= self.model.datetime,
            self.model.status == StatusAppointmentEnum.IN_QUEUE,
            self.model.doctor_id == doctor_id
        ).count()

    
