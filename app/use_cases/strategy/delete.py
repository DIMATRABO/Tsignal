from models.model import Strategy
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Delete:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, strategy:Strategy , user_id: str):
        with self.sessionContext as session:
            strategy = self.repo.getStrategyById(session, strategy.id)
            return self.repo.deleteUsersStrategy(session, strategy, user_id)
    