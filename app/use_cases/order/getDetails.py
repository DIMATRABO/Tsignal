from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.dataBaseSession.sessionContext import SessionContext


class GetDetails:
    def __init__(self , order_repo , strategy_repo , account_repo ):
        self.order_repo = order_repo
        self.strategy_repo = strategy_repo
        self.account_repo = account_repo
        self.sessionContext = SessionContext()

    def handle(self, order_id:str):
        with self.sessionContext as session : 
            order = self.order_repo.getOrderById(session , order_id)
            strategy = self.strategy_repo.getStrategyById(session ,order.strategy_id)
            account = self.account_repo.getAccountById(session , strategy.account_id)
            exchange = ExchangeExecution(account.exchange.id, account.key)
            response = exchange.getOrderDetails(order_id)
            return response



 