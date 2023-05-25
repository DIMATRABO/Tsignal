
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, getUserInput):
        with self.sessionContext as session : 
            if not getUserInput.id is None :
                user = self.repo.getUserById(session , getUserInput.id)
            if not getUserInput.login is None and not getUserInput.passwd is None :
                user = self.repo.getUserByEmailPasswd(session , getUserInput.login , getUserInput.passwd)    
            return user
