from models.model import Subscription
import uuid
import string
from gate_ways.dataBaseSession.sessionContext import SessionContext
from datetime import datetime
import secrets


class Subscribe:
    def __init__(self ,  subscription_repp ,public_strategy_repo, account_repo):
        self.repo=subscription_repp
        self.public_strategy_repo = public_strategy_repo
        self.account_repo = account_repo
        self.sessionContext = SessionContext()
        self.key_lenght = 32
    
    def handle(self, subscription:Subscription):
        with self.sessionContext as session:
            if(not self.account_repo.user_have_account(session, subscription.user_id, subscription.account_id)):
                raise Exception("account not found")
            if(self.public_strategy_repo.getPublicStrategyById(session, subscription.strategy_id) is None):
                raise Exception("strategy not found")

            subscription.id = str(uuid.uuid4())
            subscription.webhook_id = str(uuid.uuid4())
            subscription.created_at = datetime.now()
            charset = string.ascii_letters + string.digits
            subscription.webhook_key = ''.join(secrets.choice(charset) for _ in range(self.key_lenght))

            return self.repo.save(session , subscription)
             

   