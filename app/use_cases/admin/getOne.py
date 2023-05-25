
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, getAdminInput):
        with self.sessionContext as session : 
            if not getAdminInput.id is None :
                admin = self.repo.getAdminById(session , getAdminInput.id)
            if not getAdminInput.login is None and not getAdminInput.passwd is None :
                admin = self.repo.getAdminByLoginPasswd(session , getAdminInput.login , getAdminInput.passwd)    
            return admin
