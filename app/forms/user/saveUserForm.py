from datetime import date , datetime
from models.model import User

class SaveUserForm:
    login:str
    password:str
    first_name: str 
    last_name: str 
    birthday: date

    def __init__(self , jsonUser):
        if(  not "login" in  jsonUser):
            raise Exception("login required")
        else:
            self.login=jsonUser["login"]
        
        if(  not "password" in  jsonUser):
            raise Exception("password required")
        else:
            self.password=jsonUser["password"]
    
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
            login=self.login,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday
        )