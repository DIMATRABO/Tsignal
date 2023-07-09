from models.model import User
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Activate:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, user_id):
        with self.sessionContext as session:
            user = self.repo.getUserById(session, user_id)
            return self.repo.update(session , user)
    