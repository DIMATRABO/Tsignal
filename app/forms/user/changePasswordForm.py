from forms.validator import Validator

class ChangePasswordForm:
    last_password:str
    new_password:str
    password_confirm:str

      

    def __init__(self , jsonUser):

        validator = Validator()


        if(  not "last_password" in  jsonUser):
            raise Exception("last_password required")
        else:
            self.last_password=jsonUser["last_password"]

        if(  not "new_password" in  jsonUser):
            raise Exception("new_password required")
        else:
            self.new_password=jsonUser["new_password"]
            validator.validate_password(self.new_password)
        
        if(  not "password_confirm" in  jsonUser):
            raise Exception("password_confirm required")
        else:
            self.password_confirm=jsonUser["password_confirm"]

        if( self.new_password != self.password_confirm):
            raise Exception("new_password and password_confirm does not  match")


