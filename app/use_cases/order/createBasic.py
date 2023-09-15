from models.model import Order
from forms.order.createBasicOrder import CreateBasicOrderForm

from use_cases.utils.map_exchange_response import map_data

import uuid
from gate_ways.dataBaseSession.sessionContext import SessionContext
from gate_ways.account.secretsManager import SecretRepo
from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.log import Log
from datetime import datetime


logger = Log()


class CreateBasic:
    def __init__(self ,  orderRepo , accountRepo , strategyRepo ):
        self.orderRepo = orderRepo
        self.accountRepo = accountRepo
        self.strategyRepo = strategyRepo
        self.sessionContext = SessionContext()
        self.secretRepo = SecretRepo()




    def handle(self, basicOrder:CreateBasicOrderForm , webhookId:str):
        with self.sessionContext as session:
            strategy = self.strategyRepo.getStrategyByWebhookId(session , webhookId)
            if not strategy is None:
                if strategy.webhook_key == basicOrder.key:

                    order = Order(
                        id= str(uuid.uuid4()),
                        strategy_id=webhookId,
                        is_buy= basicOrder.side == "BUY",
                        is_future=strategy.is_future,
                        is_limit=False,
                        symbol=strategy.symbol,
                        symbol_id=strategy.symbol_id,
                        amount=strategy.entry_size,
                        reception_date=datetime.now()
                        )
                
                    account = self.accountRepo.getAccountById(session , strategy.account_id)
                    if not account is None:
                        account.key = self.secretRepo.read(account.key_id)
                        exchange = ExchangeExecution(account.exchange.id , account.key)
                        response = exchange.executeOrder(order)
                        
                        if "id" in response:
                            response = exchange.getOrderDetails(response['id'], order.symbol_id)

                        order = map_data(order=order , response=response)

                        self.orderRepo.save(session, order)
                        logger.log(response)
                        return response
                    else:
                        raise  Exception("unkown account")
                else :
                    raise  Exception("invalide key")
            else :
                raise  Exception("unkown strategy")



