from models.model import Strategy
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Delete:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, strategy:Strategy):
        with self.sessionContext as session:
            return self.repo.delete(session , strategy)
    