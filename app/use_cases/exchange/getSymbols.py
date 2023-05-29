from gate_ways.integration.exchangeExecution import ExchangeExecution
from datetime import datetime



class GetSymbols:
          

    def handle(self, exchange_id):     
        exchange = ExchangeExecution(exchange_id=exchange_id)
        return exchange.symbols()