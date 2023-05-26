
from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.account.secretsManager import SecretRepo
from gate_ways.dataBaseSession.sessionContext import SessionContext

secret_repo = SecretRepo() 

class GetBalance:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()
      
    def handle(self, user_id , account_id , currency):
        with self.sessionContext as session : 
            
            account = self.repo.getAccountById(session , account_id)
            if( account.user_id == user_id):
                execution = ExchangeExecution(exchange_id=account.exchange.id ,key = secret_repo.read(account_id))
                return execution.available_balance(currency)
            else:
                raise Exception("unauthorized")
                 