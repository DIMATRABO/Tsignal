
class AuthUserForm:
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
            #if(  len(jsonCredentials["password"]) <8):
            #    raise Exception("password must be have more then 8 characters")
            #else:
                self.password=jsonCredentials["password"]



  