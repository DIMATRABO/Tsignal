from models.model import Account
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Delete:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, account:Account , user_id:str):
        with self.sessionContext as session:
            return self.repo.delete(session , account , user_id)
    