from models.model import Subscription
import uuid
from gate_ways.dataBaseSession.sessionContext import SessionContext
from datetime import datetime

class Unsubscribe:
    def __init__(self ,  subscription_rep ,public_strategy_repo, account_repo):
        self.repo=subscription_rep
        self.public_strategy_repo = public_strategy_repo
        self.account_repo = account_repo
        self.sessionContext = SessionContext()


    
    def handle(self, subscription:Subscription):
        with self.sessionContext as session:
            if(not self.account_repo.user_have_account(session, subscription.user_id, subscription.account_id)):
                raise Exception("account not found")
            if(self.public_strategy_repo.getStrategyByWebhookId(session, subscription.strategy_id) is None):
                raise Exception("strategy not found")
            

            unsubscribe = self.repo.unsubscribe(session , subscription.user_id, subscription.strategy_id , subscription.account_id)
            if(unsubscribe is None):
                raise Exception("no subscription found")
            
            return unsubscribe
                
   