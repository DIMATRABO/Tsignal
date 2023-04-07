from models.model import Order, Account
from json import dumps
import uuid
from gate_ways.dataBaseSession.sessionContext import SessionContext
from threading import Thread
from gate_ways.account.secretsManager import SecretRepo
from gate_ways.integration.exchangeExecution import ExchangeExecution
from gate_ways.log import Log


logger = Log()


class Create:
    def __init__(self ,  orderRepo , accountRepo ):
        self.orderRepo=orderRepo
        self.accountRepo=accountRepo
        self.sessionContext = SessionContext()
        self.secretRepo = SecretRepo()



       
            
    def accountTreatment(self, order:Order , account:Account):
        try:
            order.account_id = account.id
            order.id = str(uuid.uuid4())
            with self.sessionContext as session:
                self.orderRepo.save(session, order)
            
            account.key = self.secretRepo.read(account.key_id)
            exchange = ExchangeExecution(account.exchange.id , account.key)
            response = exchange.executeOrder(order)
            logger.log(response)
        except Exception as e :
            json_data = dumps({"status_message":str(e)})
            logger.log(json_data)
       


        



    def handle(self, order:Order):
        with self.sessionContext as session:
            accounts = self.accountRepo.getAllAccounts(session)
        i = 0
        for account in accounts:
            thread = Thread(target=self.accountTreatment , args=( order , account ))
            thread.start()
            i+=1
        return i






 