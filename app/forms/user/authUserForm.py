from models.model import User

class AuthUserForm:
    login: str 
    passwd:str
    

    def __init__(self , jsonCredentials):
    
        if(  not "login" in  jsonCredentials):
            raise Exception("login required")
        else:
            self.login=jsonCredentials["login"]

        if(  not "passwd" in  jsonCredentials):
            raise Exception("passwd required")
        else:
            if(  len(jsonCredentials["passwd"]) <8):
                raise Exception("passwd must be have more then 8 characters")
            else:
                self.passwd=jsonCredentials["passwd"]



  