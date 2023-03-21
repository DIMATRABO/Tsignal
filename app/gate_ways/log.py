import logging
from gate_ways.config_handler import Config_handler

class Log:
    log_file:str

    def __init__(self):
        config = Config_handler()
        self.log_file = config.get_log_file()
        logging.basicConfig(filename=self.log_file ,level= logging.DEBUG ,format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
    
    def log(self , message):
        logging.info(message)







