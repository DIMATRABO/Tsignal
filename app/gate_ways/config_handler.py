import yaml
import os


class Config_handler :
    
    def __init__(self):
        cwd = os.getcwd()
        self.config_file = os.path.abspath(os.path.join(cwd, "../config/production.yml"))
        with open(self.config_file, "r") as f:
            self.data = yaml.safe_load(f)
            self.is_production=self.data["environment"]['is_production']
        if(self.is_production  == False):
            self.config_file = os.path.abspath(os.path.join(cwd, "../config/test.yml"))
            with open(self.config_file, "r") as f:
                self.data = yaml.safe_load(f)
    

    def get_db_host(self):
        return self.data["database"]['host']
    
    def get_db_port(self):
        return self.data["database"]['port']

    def get_db_name(self):
        return self.data["database"]['name']

    def get_db_user(self):
        return self.data["database"]['user']
    
    def get_db_passwd(self):
        return self.data["database"]['password']



    def get_log_file(self):
        return self.data["logging"]['filename']

    def get_log_level(self):
        return self.data["logging"]['level']
    

    def get_app_name(self):
        return self.data["app"]["name"]
    
    def get_app_host(self):
        return self.data["app"]["host"]
    
    def get_app_port(self):
        return self.data["app"]["port"]
    
    def get_app_debug_mode(self):
        return self.data["app"]["debug"]
    
    

    def get_jwt_secret(self):
        return self.data["jwt"]["secret"]
    
    def get_jwt_expiration(self):
        return int(self.data["jwt"]["expiration"])
    
    


