
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,getStrategiesInput):
        with self.sessionContext as session:
            if not getStrategiesInput.all is None :
                to_return = self.repo.getAllStrategies(session )
            if not getStrategiesInput.account_id is  None : 
                to_return = self.repo.getAllByAccountId(session, getStrategiesInput.account_id)
            
            return to_return



