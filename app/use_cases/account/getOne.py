
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, getAccountInput):
        with self.sessionContext as session : 
            if not getAccountInput.id is None :
                account = self.repo.getAccountById(session , getAccountInput.id)
     
            return account
