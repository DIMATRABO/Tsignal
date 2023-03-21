
from gate_ways.config_handler import Config_handler
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

class SessionContext:

    def __init__(self):
        config = Config_handler()
        dbname = config.get_db_name()
        user = config.get_db_user()
        password = config.get_db_passwd()
        port = config.get_db_port()
        host = config.get_db_host()
        engine = create_engine("postgresql+psycopg2://"+ user+":"+ password+"@"+host+":"+str(port)+"/"+dbname)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def __enter__(self):
        return self.session


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()