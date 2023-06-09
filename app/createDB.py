from gate_ways.alchemy_db_create import Db_creator
from gate_ways.config_handler import Config_handler
from gate_ways.exchange.sqlalchimyRepo import SqlAlchimy_repo as Exchange_repo
from use_cases.exchange.save import Save
from models.model import Exchange

#creating database
config = Config_handler()
pg = Db_creator(config)
pg.create()






exchange_repo = Exchange_repo()
saving_handler = Save(exchange_repo)

exchanges = []
binance = Exchange(id="binance",
                    name="Binance",
                    image="https://th.bing.com/th/id/R.ff9e0bf3f6594ce90f7e244ed01f3249?rik=CmDLd8saAlC9Cw&pid=ImgRaw&r=0"
                    )


exchanges.append(binance)

kucoin = Exchange(id="kucoin",
                    name="Kucoin",
                    image="https://th.bing.com/th/id/R.7977276c639bb8bc640af3b9afc0a864?rik=2Jzfnzj%2fLOXvow&pid=ImgRaw&r=0"
                    )


exchanges.append(kucoin)

bybit = Exchange(id="bybit",
                    name="Bybit",
                    image="https://th.bing.com/th/id/OIP.RxhSjRFe38GxfJ5phvUOewAAAA?pid=ImgDet&w=474&h=276&rs=1"
                    )


exchanges.append(bybit)

for exchange in exchanges:
    saving_handler.handle(exchange=exchange)