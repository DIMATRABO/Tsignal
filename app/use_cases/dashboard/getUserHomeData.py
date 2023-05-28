
from gate_ways.dataBaseSession.sessionContext import SessionContext
from forms.dashboard.userHomeResponse import UserHomeResponse

class GetUserHomeData:
    def __init__(self ,  order_repo ):
        self.order_repo=order_repo
        self.sessionContext = SessionContext()

    def handle(self , user_id):
        with self.sessionContext as session : 
            data = UserHomeResponse()

            data.total_orders = self.order_repo.getTotalOrdersByUserId(session, user_id)
            data.total_buy_orders = self.order_repo.getTotalBuyOrdersByUserId(session, user_id)
            data.total_sell_orders= self.order_repo.getTotalSellOrdersByUserId(session, user_id)
            #data.average_sell_price= self.order_repo.getAverageSellpriceByUserId(session, user_id)
            #data.average_buy_price= self.order_repo.getAverageBuyPriceByUserId(session, user_id)
            data.total_sell_quantitiy= self.order_repo.getTotalSellQuantityByUserId(session, user_id)
            data.total_buy_quantity= self.order_repo.getTotalBuyQuantityByUserId(session, user_id)
            data.monthly_profit = [0 for _ in range(12)]

            return data
             
