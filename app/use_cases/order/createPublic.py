from models.model import Order, Account

from use_cases.utils.map_exchange_response import map_data

import uuid
from gate_ways.dataBaseSession.sessionContext import SessionContext
from gate_ways.account.secretsManager import SecretRepo
from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.log import Log
from datetime import datetime

from threading import Thread
from json import dumps

logger = Log()


class CreatePublic:
    def __init__(self ,  orderRepo , accountRepo , publicStrategyRepo):
        self.orderRepo = orderRepo
        self.accountRepo = accountRepo
        self.publicStrategyRepo = publicStrategyRepo
        self.sessionContext = SessionContext()
        self.secretRepo = SecretRepo()



    def accountTreatment(self, order:Order , account:Account , subscription_id:str):
        try:
            order.account_id = account.id
            order.id = str(uuid.uuid4())
            order.subscription_id = subscription_id
            account.key = self.secretRepo.read(account.key_id)
            exchange = ExchangeExecution(account.exchange.id , account.key)
            response = exchange.executeOrder(order)
            if "id" in response:
                response = exchange.getOrderDetails(response['id'] , order.symbol_id)
            order = map_data(order=order , response=response)
            with self.sessionContext as session:
                self.orderRepo.save(session, order)
            logger.log(response)
            
        except Exception as e :
            json_data = dumps({"status_message":str(e)})
            logger.log(json_data)
       



    
    def handle(self, order: Order, key: str):
        with self.sessionContext as session:
            publicStrategy = self.publicStrategyRepo.getStrategyByWebhookId(session, order.strategy_id)
            if publicStrategy is not None:
                if publicStrategy.webhook_key == key:
                    order.reception_date = datetime.now()
                    account_subscriptions = self.accountRepo.getActifAccountsByPublicStrategyId(session, publicStrategy.webhook_id)
                    i = 0
                    for account, subscription_id in account_subscriptions:
                        thread = Thread(target=self.accountTreatment, args=(order, account, subscription_id))
                        thread.start()
                        i += 1
                    return {"executed": i}
                else:
                    raise Exception("Invalid key")
            else:
                raise Exception("Unknown strategy")

        
    