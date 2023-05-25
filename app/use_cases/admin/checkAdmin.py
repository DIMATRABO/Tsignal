
from gate_ways.dataBaseSession.sessionContext import SessionContext
class CheckAdmin:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, admin_id, login , privilege, must_have_privilege):
        exist = False
        have_privilege = False
        
        with self.sessionContext as session : 
            admin = self.repo.getAdminByIdAndLoginAndPrivilege(session, admin_id, login , privilege)
            if not admin is None:
                exist = True
            if privilege == must_have_privilege:
                have_privilege = True

        return exist and have_privilege
