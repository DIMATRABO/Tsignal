
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

            return data
             
