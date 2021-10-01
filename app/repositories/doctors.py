from .base import BaseRepository

class DoctorsRepository(BaseRepository):

    def firstByUsername(self, username: str):
        return self.firstBy({"username": username})

    
