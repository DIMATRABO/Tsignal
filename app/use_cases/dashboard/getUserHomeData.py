
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
            data.average_sell_price= self.order_repo.getAverageSellPriceByUserId(session, user_id)
            data.average_buy_price= self.order_repo.getAverageBuyPriceByUserId(session, user_id)
            data.total_sell_quantitiy= self.order_repo.getTotalSellQuantityByUserId(session, user_id)
            data.total_buy_quantity= self.order_repo.getTotalBuyQuantityByUserId(session, user_id)
           
            data.total_failed_orders = self.order_repo.getTotalFailedOrdersByUserId(session, user_id)
           
            income = self.order_repo.getTotalIncomeByMonthByUser(session, user_id)
            invested = self.order_repo.getTotalInvestedByMonthByUser(session, user_id)

            for i in range(len(income)):
                data.monthly_profit.append(income[i] - invested[i])  # Subtract B(i) from A(i) and add the result to the list


            data.orders_by_strategy = self.order_repo.get_total_trades_by_strategy(session, user_id)

            return data
             
