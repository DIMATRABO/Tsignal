from models.model import Account
import uuid
from gate_ways.dataBaseSession.sessionContext import SessionContext
from gate_ways.account.secretsManager import SecretRepo
from datetime import datetime
from gate_ways.integration.exchangeExecution import ExchangeExecution


class Save:
    def __init__(self ,  repo ):
        self.repo=repo
        self.sessionContext = SessionContext()
        self.secretRepo = SecretRepo()
    
    def handle(self, account:Account , user_id):
        with self.sessionContext as session:
            account.user_id = user_id
            account.created_at = datetime.now()
            account.key_id = str(uuid.uuid4())
            self.secretRepo.save(account.key_id  ,account.key)

            exchange_repo = ExchangeExecution(account.exchange.id, account.key)
            account.balance = exchange_repo.available_balance(account.currency)

            to_return = self.repo.save(session , account)
            return to_return

