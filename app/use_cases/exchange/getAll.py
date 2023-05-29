
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,getAllInput):
        with self.sessionContext as session:
            if ( not getAllInput.all !=None ): 
                return  self.repo.getAll(session)
          
            


