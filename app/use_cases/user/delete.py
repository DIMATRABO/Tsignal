from models.model import User
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Delete:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, user:User):
        with self.sessionContext as session:
            return self.repo.delete(session , user)
    