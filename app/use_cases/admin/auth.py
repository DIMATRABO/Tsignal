from forms.admin.authAdminForm import AuthAdminForm
import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext

class Auth:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, authForm:AuthAdminForm):
        with self.sessionContext as session:
            admin = self.repo.getAdminByLogin(session , authForm.login)
            if not admin is None:
                if bcrypt.checkpw(
                    authForm.password.encode('utf-8'),
                    admin.password.encode('utf-8')
                    ):
                    return admin
            return None

