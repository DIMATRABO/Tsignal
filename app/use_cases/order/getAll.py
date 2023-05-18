
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,getOrdersInput):
        with self.sessionContext as session:
            if not getOrdersInput.webhook_id is  None : 
                to_return = self.repo.getAllByStrategyId(session, getOrdersInput.webhook_id)
            return to_return



