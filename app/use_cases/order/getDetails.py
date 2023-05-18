from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.log import Log


logger = Log()


class GetDetails:
    def __init__(self):
        pass


    def handle(self, order_id:str):
        key = {
                "apiKey": "646391e8ce9a090001908eda",
                "password": "tsignal",
                "secret": "9b8eab36-18b9-4dca-b24b-ecd3f1e37777"
                }
        exchange = ExchangeExecution("kucoin", key)
        response = exchange.getOrderDetails(order_id)
        return response



 