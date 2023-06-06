
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
            
            income  = self.order_repo.getTotalIncomeByMonthByStrategyAndUser(session, user_id, strategy_id)
            invested = self.order_repo.getTotalInvestedByMonthByStrategyAndUser(session, user_id, strategy_id)

            for i in range(len(income)):
                data.monthly_profit.append(income[i] - invested[i])  # Subtract B(i) from A(i) and add the result to the list


            data.orders_by_trading_pair = self.order_repo.get_total_trades_by_pair(session, user_id, strategy_id)

            return data
        
        
             
