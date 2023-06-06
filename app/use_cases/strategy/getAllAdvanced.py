
from gate_ways.dataBaseSession.sessionContext import SessionContext
from forms.strategy.strategyResponseForm import StrategyResponseForm

class GetAllAdvanced:
    def __init__(self , strategy_repo, account_repo,order_repo):
        self.strategy_repo = strategy_repo
        self.account_repo = account_repo
        self.order_repo = order_repo
        self.sessionContext = SessionContext() 

    def handle(self  , user_id):
        with self.sessionContext as session:
            strategies  = self.strategy_repo.getAllByUserId(session , user_id)
            advanced = []
            for strategy in strategies:
                responseForm = StrategyResponseForm(strategy)
                account = self.account_repo.getAccountById(session , strategy.id)
                responseForm.account_name = None if account is None else account.name
                responseForm.nb_orders_7days = self.order_repo.getTotalOrdersByStrategyAndUserIdLast7Days(session, user_id , strategy.webhook_id)
                responseForm.income_7_days = self.order_repo.getTotalIncomeLast7DaysByStrategyAndUser(session, user_id , strategy.webhook_id)
                responseForm.invested_7_days = self.order_repo.getTotalInvestedLast7DaysByStrategyAndUser(session, user_id , strategy.webhook_id)
                advanced.append(responseForm)
            return advanced
        





