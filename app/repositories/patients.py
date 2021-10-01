from .base import BaseRepository

class PatientsRepository(BaseRepository):

    def firstByNoKTP(self, no_ktp: str):
        return self.firstBy({"no_ktp": no_ktp})

    
