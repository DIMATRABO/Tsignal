
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, getStrategyInput):
        with self.sessionContext as session : 
            if ( not getStrategyInput.id is None ) and getStrategyInput.user_id is None:
                strategy = self.repo.getStrategyById(session , getStrategyInput.id)
     
            if ( not getStrategyInput.id is None ) and ( not getStrategyInput.user_id is None):
                strategy = self.repo.getStrategyByIdAndUserId(session , getStrategyInput.id, getStrategyInput.user_id)
     
            return strategy
