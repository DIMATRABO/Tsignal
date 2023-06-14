
from gate_ways.dataBaseSession.sessionContext import SessionContext

class GetAllPaginated:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self, getOrdersInput, page_number, page_size):
        with self.sessionContext as session:
            if ( not getOrdersInput.webhook_id is None ) and (not getOrdersInput.user_id is None): 
                to_return = self.repo.getAllByStrategyIdAndUserIdPaginated(
                    session, getOrdersInput.webhook_id, None, page_number, page_size
                )
            if ( getOrdersInput.webhook_id is None ) and (not getOrdersInput.user_id is None): 
                 to_return = self.repo.getAllByUserIdPaginated(
                    session, getOrdersInput.user_id, page_number, page_size
                )
            return to_return

