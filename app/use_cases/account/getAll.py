
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self ,  repo , exchange_repo):
        self.repo=repo
        self.exchange_repo = exchange_repo
        self.sessionContext = SessionContext()

    def handle(self  ,getAccountsInput):
        with self.sessionContext as session:
            if not getAccountsInput.all is None :
                accounts = self.repo.getAllAccounts(session )
            if not getAccountsInput.user_id is  None : 
                accounts = self.repo.getAllByUserId(session, getAccountsInput.user_id)
            if not getAccountsInput.exchange_id is  None : 
                accounts = self.repo.getAllByExchangeId(session , getAccountsInput.exchange_id)  

            for account  in  accounts:
                account.exchange = self.exchange_repo.getById(session , account.exchange_id)

            return accounts



