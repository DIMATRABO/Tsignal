from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.dataBaseSession.sessionContext import SessionContext
from gate_ways.account.secretsManager import SecretRepo


class GetDetails:
    def __init__(self , order_repo , strategy_repo , account_repo ):
        self.order_repo = order_repo
        self.strategy_repo = strategy_repo
        self.account_repo = account_repo
        self.sessionContext = SessionContext()
        self.secretRepo = SecretRepo()

    def handle(self, order_id:str):
        with self.sessionContext as session : 
            
            order = self.order_repo.getOrderById(session , order_id)
            if order is None:
                raise Exception("Order Not found")
            
            if order.execution_id is None:
                raise Exception("The order has not been executed")
            
            strategy = self.strategy_repo.getStrategyByWebhookId(session ,order.strategy_id)
            if strategy is None:
                raise Exception("Unknown Strategy")
            account = self.account_repo.getAccountById(session , strategy.account_id)
            if account is None:
                raise Exception("Unknown wallet")
            account.key = self.secretRepo.read(account.key_id)
            exchange = ExchangeExecution(account.exchange.id, account.key)
            response = exchange.getOrderDetails(order.execution_id , order.symbol_id)
            return response



 