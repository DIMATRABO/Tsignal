
from gate_ways.dataBaseSession.sessionContext import SessionContext
class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handel(self  ,user ,getUsersInput):
        with self.sessionContext as session:
            if not getUsersInput.all is None :
                to_return = self.repo.getAllUsers(session , user)
            if not getUsersInput.first_name is  None : 
                to_return = self.repo.getAllByFirstName(session , user , getUsersInput.first_name)
            if not getUsersInput.last_name is  None : 
                to_return = self.repo.getAllByLastName(session  , user , getUsersInput.last_name)  
            return to_return



