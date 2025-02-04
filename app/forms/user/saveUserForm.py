from datetime import date , datetime
from models.model import User
from forms.validator import Validator
class SaveUserForm:
    email:str
    password:str
    password_confirm:str
    first_name: str 
    last_name: str 
    birthday: date

    def __init__(self , jsonUser):

        validator = Validator()

        if(  not "email" in  jsonUser):
            raise Exception("email required")
        else:
            self.email=jsonUser["email"]
            validator.validate_email_format(self.email)
        
        if(  not "password" in  jsonUser):
            raise Exception("password required")
        else:
            self.password=jsonUser["password"]
            validator.validate_password(self.password)


        if(  not "password_confirm" in  jsonUser):
            raise Exception("password_confirm required")
        else:
            self.password_confirm=jsonUser["password_confirm"]

        if( self.password != self.password_confirm):
            raise Exception("password and password_confirm does not  match")

    
        if(  not "first_name" in  jsonUser):
            raise Exception("first_name required")
        else:
            self.first_name=jsonUser["first_name"]
        if(  not "last_name" in  jsonUser):
            raise Exception("last_name required")
        else:
            self.last_name=jsonUser["last_name"]
        if(  not "birthday" in  jsonUser):
            raise Exception("birthday is required")
        try:
            self.birthday = datetime.strptime(jsonUser["birthday"] , "%Y-%m-%d")
        except ValueError:
            raise Exception("The birthday is not a date")
        

        


    def to_domain(self):
        return User(
            id=None,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday            
        )