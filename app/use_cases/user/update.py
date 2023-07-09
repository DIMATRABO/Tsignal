from models.model import User
from gate_ways.dataBaseSession.sessionContext import SessionContext
class Update:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handle(self, user:User):
        with self.sessionContext as session:
            user_ = self.repo.getUserById(session, user.id)
            user_ = self.patchUser(user_ , user)
            return self.repo.update(session , user_)
    



    
    def patchUser(self, old_user:User , new_user:User):
        
        # Update the non-null fields of the user entity
        if new_user.email is not None:
            old_user.email = new_user.email
        if new_user.first_name is not None:
            old_user.first_name = new_user.first_name
        if new_user.last_name is not None:
            old_user.last_name = new_user.last_name
        if new_user.birthday is not None:
            old_user.birthday = new_user.birthday

        
        return old_user