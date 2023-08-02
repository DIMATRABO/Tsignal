from gate_ways.dataBaseSession.sessionContext import SessionContext
class ChangeState:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, user_id):
        with self.sessionContext as session:
            user = self.repo.getUserById(session, user_id)
            if not user is None :
                user.is_actif = not user.is_actif
            return self.repo.update(session , user)
    