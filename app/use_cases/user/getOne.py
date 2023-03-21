
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, getUserInput):
        with self.sessionContext as session : 
            if not getUserInput.uuid is None :
                user = self.repo.getUserById(session , getUserInput.uuid)
            if not getUserInput.login is None and not getUserInput.passwd is None :
                user = self.repo.getUserByLoginPasswd(session , getUserInput.login , getUserInput.passwd)    
            return user
