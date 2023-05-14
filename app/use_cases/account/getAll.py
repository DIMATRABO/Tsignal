
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,getAccountsInput):
        with self.sessionContext as session:
            if not getAccountsInput.all is None :
                to_return = self.repo.getAllAccounts(session )
            if not getAccountsInput.user_id is  None : 
                to_return = self.repo.getAllByUserId(session, getAccountsInput.user_id)
            if not getAccountsInput.exchange_id is  None : 
                to_return = self.repo.getAllByExchangeId(session , getAccountsInput.exchange_id)  
            return to_return



