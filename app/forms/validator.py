
import re

class Validator:
      
      def validate_email_format(self, email):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise Exception("invalid email format")
        
      def validate_password(self, password):
          if(  len(password) <8 ):
                raise Exception("password must be have more then 8 characters")
          
  