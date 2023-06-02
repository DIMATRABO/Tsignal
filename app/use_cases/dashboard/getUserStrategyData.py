
from gate_ways.dataBaseSession.sessionContext import SessionContext
from forms.dashboard.userStrategyResponse import UserStrategyResponse

class GetUserStrategyData:
    def __init__(self ,  order_repo ):
        self.order_repo=order_repo
        self.sessionContext = SessionContext()

    def handle(self , user_id, strategy_id):
        with self.sessionContext as session : 
            data = UserStrategyResponse()

            data.total_orders = self.order_repo.getTotalOrdersByStrategyAndUserId(session, user_id, strategy_id)
            data.total_buy_orders = self.order_repo.getTotalBuyOrdersByStrategyAndUserId(session, user_id, strategy_id)
            data.total_sell_orders= self.order_repo.getTotalSellOrdersByStrategyAndUserId(session, user_id, strategy_id)
            data.average_sell_price= self.order_repo.getAverageSellPriceByStrategyAndUserId(session, user_id, strategy_id)
            data.average_buy_price= self.order_repo.getAverageBuyPriceByStrategyAndUserId(session, user_id, strategy_id)
            data.total_sell_quantitiy= self.order_repo.getTotalSellQuantityByStrategyAndUserId(session, user_id, strategy_id)
            data.total_buy_quantity= self.order_repo.getTotalBuyQuantityByStrategyAndUserId(session, user_id, strategy_id)
           
            data.total_failed_orders = self.order_repo.getTotalFailedOrdersByStrategyAndUserId(session, user_id, strategy_id)
            
            data.monthly_profit = self.order_repo.getTotalIncomeByMonthByStrategyAndUser(session, user_id, strategy_id)
            data.monthly_invested = self.order_repo.getTotalInvestedByMonthByStrategyAndUser(session, user_id, strategy_id)

            data.orders_by_trading_pair = self.order_repo.get_total_trades_by_pair(session, user_id, strategy_id)

            return data
        
        
             
