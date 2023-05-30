from gate_ways.integration.exchangeExecution import ExchangeExecution
from datetime import datetime



class GetQuotes:
          

    def handle(self, exchange_id):     
        exchange = ExchangeExecution(exchange_id=exchange_id)
        return exchange.quotes()