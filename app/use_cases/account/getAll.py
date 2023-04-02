
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,account ,getAccountsInput):
        with self.sessionContext as session:
            if not getAccountsInput.all is None :
                to_return = self.repo.getAllAccounts(session , account)
            if not getAccountsInput.account_id is  None : 
                to_return = self.repo.getAllByAccountId(session , account , getAccountsInput.account_id)
            if not getAccountsInput.exchange_id is  None : 
                to_return = self.repo.getAllByExchangeId(session  , account , getAccountsInput.exchange_id)  
            return to_return



