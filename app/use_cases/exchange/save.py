from models.model import Exchange
from gate_ways.dataBaseSession.sessionContext import SessionContext

class Save:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()
    
  
    def handle(self, exchange:Exchange):
        with self.sessionContext as session:
            return self.repo.save(session , exchange)
             

