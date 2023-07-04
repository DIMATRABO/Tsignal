
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,getStrategiesInput, page_number, page_size):
        with self.sessionContext as session:
            if not getStrategiesInput.all is None :
                to_return = self.repo.getAllPaginated(session, page_number, page_size)
            if not getStrategiesInput.account_id is  None : 
                to_return = self.repo.getAllByAccountId(session, getStrategiesInput.account_id, page_number, page_size)
            if not getStrategiesInput.user_id is  None : 
                to_return = self.repo.getAllByUserId(session, getStrategiesInput.user_id, page_number, page_size)
            
            return to_return



