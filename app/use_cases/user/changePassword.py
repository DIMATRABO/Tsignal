import bcrypt
from gate_ways.dataBaseSession.sessionContext import SessionContext

class ChangePassword:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, user_id , old_password , new_password):
        with self.sessionContext as session:
            user = self.repo.getUserById(session , user_id)
          
            if  bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
                new_password_encrypted = (bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())).decode("utf-8") 
                user.password = new_password_encrypted
                return self.repo.update(session , user)
            else:
                raise Exception("unauthorized ")
    