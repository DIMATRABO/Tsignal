import ccxt
from models.model import Order


class ExchangeExecution:

    def __init__(self, exchange_id , key=None):
        if key is None:
            exchange_class = getattr(ccxt, exchange_id)
            self.exchange = exchange_class()
        else:
            self.exchange = getattr(ccxt, exchange_id)(key)

  
        
    def get_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except ccxt.ExchangeError as e:
            return {"error":str(e)}
        


    def available_balance(self , asset):
        try:
            balance = self.exchange.fetch_balance()
            if asset in balance:
                balance = float(balance[asset]['free'])
            else:
                balance = 0
            return balance
        except ccxt.ExchangeError as e:
            return None
        


    def buy(self, symbol, qty, price=None, order_type='limit'):
        if order_type == 'limit':
            try:
                order = self.exchange.create_order(symbol, 'limit', 'buy', qty, price)
                return order
            except ccxt.ExchangeError as e:
                return {"error":str(e)}
        elif order_type == 'market':
            try:
                order = self.exchange.create_order(symbol, 'market', 'buy', qty)
                return order
            except ccxt.ExchangeError as e:
                return {"error":str(e)}
        else:
            return {"error": "Invalid order type"}
        

    def sell(self, symbol, qty, price=None, order_type='limit'):
        if order_type == 'limit':
            try:
                order = self.exchange.create_order(symbol, 'limit', 'sell', qty, price)
                return order
            except ccxt.ExchangeError as e:
                return {"error":str(e)}
        elif order_type == 'market':
            try:
                order = self.exchange.create_order(symbol, 'market', 'sell', qty)
                return order
            except ccxt.ExchangeError as e:
                return {"error":str(e)}
        else:
            return {"error": "Invalid order type"}
        

    def close(self, symbol):
        # This function closes the position for a given symbol
        try:
            position = self.exchange.private_get_position({'symbol': symbol})
            if position['positionAmt'] > 0:
                order = self.exchange.create_order(symbol, 'market', 'sell', abs(position['positionAmt']))
            else:
                order = self.exchange.create_order(symbol, 'market', 'buy', abs(position['positionAmt']))
            return order
        except ccxt.ExchangeError as e:
            return {"error":str(e)}
      


    def executeOrder(self ,  order: Order):
        order_type = "limit" if order.is_limit else "market"
        if order.is_buy:
            return self.buy(order.symbol_id , order.amount , order.limit_price , order_type) # ordered amount of base currency
        else:
            return self.sell(order.symbol_id , order.amount , order.limit_price , order_type) # ordered amount of base currency





    def getOrderDetails(self , order_id , symbol = None):
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order  # Do something with the order details
        except ccxt.BaseError as e:
            return (f"Error fetching order: {e}")
        
    def symbols(self):
        try:
            markets = self.exchange.load_markets()
            symbols_dict = {symbol: market['id'] for symbol, market in markets.items()}
            return symbols_dict

        except ccxt.BaseError as e:
            return (f"Error fetching symbols: {e}")
        
    def quotes(self):
        try:
            markets = self.exchange.load_markets()
            symbols_dict = {symbol: market['id'] for symbol, market in markets.items()}
            quotes = [symbol.split('/')[1] for symbol in symbols_dict.keys()]
            quotes = list(set(quotes))
            quotes_=[]
            for quote in quotes :
                if not ':' in quote:
                    quotes_.append(quote)

            return quotes_

        except ccxt.BaseError as e:
            return (f"Error fetching symbols: {e}")