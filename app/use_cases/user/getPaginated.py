from gate_ways.dataBaseSession.sessionContext import SessionContext
from use_cases.user.inputs.getAllInput import GetAllInput
class GetPaginated:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self, getAllInput:GetAllInput , page_number, page_size):
        with self.sessionContext as session:
            if ( not getAllInput.all is None):
                return self.repo.getAllPaginated(session, page_number, page_size)

            if ( not getAllInput.first_name is None) and (not getAllInput.last_name is None):
                 return self.repo.getAllByFisrtAndLastName(session , getAllInput.first_name , getAllInput.last_name , page_number, page_size)

            if ( not getAllInput.first_name is None):
                 return self.repo.getAllByFisrtName(session , getAllInput.first_name  , page_number, page_size)
            
            if ( not getAllInput.last_name is None):
                 return self.repo.getAllByLastName(session , getAllInput.last_name  , page_number, page_size)
            


          
        

