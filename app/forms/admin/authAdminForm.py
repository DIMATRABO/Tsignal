
class AuthAdminForm:
    login: str 
    password:str
    

    def __init__(self , jsonCredentials):
    
        if(  not "login" in  jsonCredentials):
            raise Exception("login required")
        else:
            self.login=jsonCredentials["login"]

        if(  not "password" in  jsonCredentials):
            raise Exception("password required")
        else:
                self.password=jsonCredentials["password"]



  