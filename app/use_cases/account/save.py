from models.model import Account
import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Save:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, account:Account):
        with self.sessionContext as session:
            to_return = self.repo.save(session , account)
            return to_return

