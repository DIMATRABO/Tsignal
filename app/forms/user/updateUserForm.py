from datetime import date , datetime
from models.model import User
from forms.validator import Validator

class UpdateUserForm:
    id:str
    email:str
    first_name: str 
    last_name: str 
    birthday: date

    def __init__(self , jsonUser):

        validator = Validator()

        if(  not "id" in  jsonUser):
            raise Exception("id required")
        else:
            self.id=jsonUser["id"]

        if(  not "email" in  jsonUser):
            raise Exception("email required")
        else:
            self.email=jsonUser["email"]
    
    
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
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday
        )