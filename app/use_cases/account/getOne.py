
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo , exchange_repo):
        self.repo=repo
        self.exchange_repo = exchange_repo
        self.sessionContext = SessionContext()

    def handle(self, getAccountInput):
        with self.sessionContext as session : 
            if not getAccountInput.id is None :
                account = self.repo.getAccountById(session , getAccountInput.id)
                account.exchange = self.exchange_repo.getById(session , account.exchange_id)
            return account
