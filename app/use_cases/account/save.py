from models.model import Account
import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Save:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, account:Account , user_id):
        with self.sessionContext as session:
            to_return = self.repo.save(session , account , user_id)
            return to_return

