from forms.user.authUserForm import AuthUserForm
import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext

class Auth:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, authForm:AuthUserForm):
        with self.sessionContext as session:
            user = self.repo.getActiveUserByEmail(session , authForm.email)
            if not user is None:
                if bcrypt.checkpw(
                    authForm.password.encode('utf-8'),
                    user.password.encode('utf-8')
                    ):
                    return user
            return None

