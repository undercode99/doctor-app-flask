from .base import BaseRepository

class EmployeesRepository(BaseRepository):

    def firstByUsername(self, username: str):
        return self.firstBy({"username": username})

    
