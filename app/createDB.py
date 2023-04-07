from gate_ways.alchemy_db_create import Db_creator
from gate_ways.config_handler import Config_handler

#creating database
config = Config_handler()
pg = Db_creator(config)
pg.create()

