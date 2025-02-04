
from gate_ways.dataBaseSession.sessionContext import SessionContext
from forms.publicStrategy.publicStrategyResponseForm import PublicStrategyResponseForm

class GetAll:
    def __init__(self , repo):
        self.repo=repo
        self.sessionContext = SessionContext() 

    def handle(self  ,getStrategiesInput, page_number, page_size):
        with self.sessionContext as session:
            if not getStrategiesInput.all is None :


                if  getStrategiesInput.all == "all_admin":
                    to_return = self.repo.getAllAdminPaginated(session, page_number, page_size)
                else :
                    to_return = self.repo.getAllPaginated(session, page_number, page_size)


            if not getStrategiesInput.account_id is  None : 
                to_return = self.repo.getAllByAccountId(session, getStrategiesInput.account_id, page_number, page_size)
            if not getStrategiesInput.user_id is  None : 
                to_return = self.repo.getAllByUserId(session, getStrategiesInput.user_id, page_number, page_size)

            if not getStrategiesInput.not_user_id is  None : 
                to_return = self.repo.getNotSubscribedPaginated(session, getStrategiesInput.not_user_id, page_number, page_size)

                
           
            to_return.strategies = [ PublicStrategyResponseForm(strategy) for strategy in to_return.strategies]

            return to_return



