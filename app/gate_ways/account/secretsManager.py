from dotenv import load_dotenv
import hvac


class SecretRepo:

    def __init__(self):
        load_dotenv()
        self.client = hvac.Client()
        if not self.client.is_authenticated():
            raise Exception("authentication to VAULT Failed")

    def save(self , secretId , data):
        self.client.secrets.kv.v2.create_or_update_secret(path=secretId, secret=data)
    
    def read(self , secretId):
        return self.client.secrets.kv.v2.read_secret_version(path=secretId)['data']['data']
