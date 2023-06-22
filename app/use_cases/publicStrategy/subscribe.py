from models.model import PublicStrategy
import uuid
import string
from gate_ways.dataBaseSession.sessionContext import SessionContext
from datetime import datetime
import secrets


class Subscribe:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()
    
    def handle(self, publicStrategy:PublicStrategy):
        with self.sessionContext as session:
            publicStrategy.id = str(uuid.uuid4())
            publicStrategy.webhook_id = str(uuid.uuid4())
            publicStrategy.created_at = datetime.now()
            charset = string.ascii_letters + string.digits
            publicStrategy.webhook_key = ''.join(secrets.choice(charset) for _ in range(self.key_lenght))

            return self.repo.save(session , publicStrategy)
             

