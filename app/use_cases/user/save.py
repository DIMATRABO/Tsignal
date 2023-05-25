from models.model import User
import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext
from datetime import datetime

class Save:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, user:User):
        with self.sessionContext as session:
            user.password = (bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())).decode("utf-8") 
            user.created_at = datetime.now()
            user.is_actif = False
            return  self.repo.save(session , user)
            

