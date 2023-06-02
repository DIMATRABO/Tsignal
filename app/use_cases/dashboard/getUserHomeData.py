
from gate_ways.dataBaseSession.sessionContext import SessionContext
from forms.dashboard.userStrategyResponse import UserStrategyResponse

class GetUserHomeData:
    def __init__(self ,  order_repo ):
        self.order_repo=order_repo
        self.sessionContext = SessionContext()

    def handle(self , user_id):
        with self.sessionContext as session : 
            data = UserStrategyResponse()

            
            data.total_orders = self.order_repo.getTotalOrdersByUserId(session, user_id)
            data.total_buy_orders = self.order_repo.getTotalBuyOrdersByUserId(session, user_id)
            data.total_sell_orders= self.order_repo.getTotalSellOrdersByUserId(session, user_id)
            data.average_sell_price= self.order_repo.getAverageSellPriceByUserId(session, user_id)
            data.average_buy_price= self.order_repo.getAverageBuyPriceByUserId(session, user_id)
            data.total_sell_quantitiy= self.order_repo.getTotalSellQuantityByUserId(session, user_id)
            data.total_buy_quantity= self.order_repo.getTotalBuyQuantityByUserId(session, user_id)
           
            data.total_failed_orders = self.order_repo.getTotalFailedOrdersByUserId(session, user_id)
           
            data.total_invisted = self.order_repo.getTotalInvistedByUser(session, user_id)
            data.total_income = self.order_repo.getTotalIncomeByUser(session, user_id)

            data.monthly_profit = self.order_repo.getTotalIncomeByMonthByUser(session, user_id)

            return data
             
