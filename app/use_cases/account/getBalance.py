
from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.dataBaseSession.sessionContext import SessionContext


class GetBalance:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()
      
    def handle(self, user_id , account_id , currency):
        with self.sessionContext as session : 
            
            account = self.repo.getAccountById(session , account_id)
            if( account.user_id == user_id):
                self.repo.loadKey(account=account)
                execution = ExchangeExecution(exchange_id=account.exchange.id ,key = account.key)
                return execution.available_balance(currency)
            else:
                raise Exception("unauthorized")
                 