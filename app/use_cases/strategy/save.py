from models.model import Strategy
import uuid
import secrets
import string
from gate_ways.dataBaseSession.sessionContext import SessionContext
from datetime import datetime

class Save:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()
        self.key_lenght = 32
  
    def handle(self, strategy:Strategy):
        with self.sessionContext as session:
            
            strategy.id = str(uuid.uuid4())

            strategy.webhook_id = str(uuid.uuid4())

            strategy.created_at = datetime.now()
            # Define the character set for the API key
            charset = string.ascii_letters + string.digits
            strategy.webhook_key = ''.join(secrets.choice(charset) for _ in range(self.key_lenght))

            return self.repo.save(session , strategy)
             

