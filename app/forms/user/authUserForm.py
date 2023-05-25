from forms.validator import Validator
class AuthUserForm:
    email: str 
    password:str
    

    def __init__(self , jsonCredentials):
        validator = Validator()
    
        if(  not "email" in  jsonCredentials):
            raise Exception("email required")
        else:
            self.email=jsonCredentials["email"]
            validator.validate_email_format(self.email)

        if(  not "password" in  jsonCredentials):
            raise Exception("password required")
        else:
            self.password=jsonCredentials["password"]
            validator.validate_password(self.password)
            
  