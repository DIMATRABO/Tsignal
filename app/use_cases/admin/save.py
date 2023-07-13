from models.model import Admin
import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext

class Save:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, admin :Admin):
        with self.sessionContext as session:
            admin.password = (bcrypt.hashpw(admin.password.encode('utf-8'), bcrypt.gensalt())).decode("utf-8") 
            return  self.repo.save(session , admin)
            

