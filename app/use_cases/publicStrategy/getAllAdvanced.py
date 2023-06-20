
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
                account = self.account_repo.getAccountById(session , strategy.account_id)
                responseForm.account_name = None if account is None else account.name


                responseForm.nb_orders_7days = self.order_repo.getTotalOrdersByStrategyAndUserIdLast7Days(session, user_id , strategy.webhook_id)
                if responseForm.nb_orders_7days is None:
                    responseForm.nb_orders_7days = 0 


                responseForm.income_7_days = self.order_repo.getTotalIncomeLast7DaysByStrategyAndUser(session, user_id , strategy.webhook_id)
                if responseForm.income_7_days is None:
                    responseForm.income_7_days = 0 


                responseForm.invested_7_days = self.order_repo.getTotalInvestedLast7DaysByStrategyAndUser(session, user_id , strategy.webhook_id)
                if responseForm.invested_7_days is None:
                    responseForm.invested_7_days = 0 

                if strategy.capital > 0:
                    responseForm.invested_7_days_percent =  responseForm.invested_7_days / strategy.capital
                    responseForm.income_7_days_percent =  responseForm.income_7_days / strategy.capital

                else:
                    responseForm.invested_7_days_percent = 0
                    responseForm.income_7_days_percent = 0

                responseForm.income_7_days = round(responseForm.income_7_days, 4)
                responseForm.invested_7_days = round(responseForm.invested_7_days, 4)
                responseForm.income_7_days_percent = round(responseForm.income_7_days_percent, 4)
                responseForm.invested_7_days_percent =round(responseForm.invested_7_days_percent, 4)


                advanced.append(responseForm)

            return advanced
        





