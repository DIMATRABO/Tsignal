
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, getStrategyInput):
        with self.sessionContext as session : 
            if not getStrategyInput.id is None :
                strategy = self.repo.getStrategyById(session , getStrategyInput.id)
     
            return strategy
