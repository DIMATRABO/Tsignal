from models.model import Subscription
import uuid
from gate_ways.dataBaseSession.sessionContext import SessionContext
from datetime import datetime

class Subscribe:
    def __init__(self ,  subscription_rep ,public_strategy_repo, account_repo):
        self.repo=subscription_rep
        self.public_strategy_repo = public_strategy_repo
        self.account_repo = account_repo
        self.sessionContext = SessionContext()
        self.key_lenght = 32
    
    def handle(self, subscription:Subscription):
        with self.sessionContext as session:
            if(not self.account_repo.user_have_account(session, subscription.user_id, subscription.account_id)):
                raise Exception("account not found")
            if(self.public_strategy_repo.getStrategyByWebhookId(session, subscription.strategy_id) is None):
                raise Exception("strategy not found")

            subscription.id = str(uuid.uuid4())
            subscription.created_at = datetime.now()
          
            return self.repo.save(session , subscription)
             

   