import ccxt
from models.model import Order


class ExchangeExecution:

    def __init__(self, exchange_id , key=None):
        self.exchange = getattr(ccxt, exchange_id)(key)

    def get_symbol(self ,exchange_id, base , quote):
        if exchange_id == "binance":
            return base+quote
        
        elif exchange_id == "kucoin":
            return base+'/'+quote
        
        elif exchange_id == "bybit":
            return base+'_'+quote
        
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
      


    def executeOrder(self ,exchange_id ,  order: Order):
        order_type = "limit" if order.is_limit else "market"
        symbol = self.get_symbol(exchange_id=exchange_id , base=order.symbol_base , quote=order.symbol_quote)
        if order.is_buy:
            return self.buy(symbol , order.amount , order.limit_price , order_type) # ordered amount of base currency
        else:
            return self.sell(symbol , order.amount , order.limit_price , order_type) # ordered amount of base currency




    def getOrderDetails(self , order_id):
        try:
            order = self.exchange.fetch_order(order_id)
            return order  # Do something with the order details
        except ccxt.BaseError as e:
            return (f"Error fetching order: {e}")
        
    def symbols(self):
        try:
            return  self.exchange.load_markets()
        
        except ccxt.BaseError as e:
            return (f"Error fetching symbols: {e}")
        