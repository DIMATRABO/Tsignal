from gate_ways.alchemy_db_create import Db_creator
from gate_ways.config_handler import Config_handler
from gate_ways.exchange.sqlalchimyRepo import SqlAlchimy_repo as Exchange_repo
from use_cases.exchange.save import Save

from gate_ways.admin.sqlalchimyRepo import SqlAlchimy_repo as Admin_repo
from use_cases.admin.save import Save as SaveAdmin


from models.model import Exchange , Admin

#creating database
config = Config_handler()
pg = Db_creator(config)
pg.create()






exchange_repo = Exchange_repo()
saving_handler = Save(exchange_repo)

admin_repo = Admin_repo()
savingAdmin_handler = SaveAdmin(admin_repo)

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




def_admin = Admin(login="anass",password='12345678',first_name="anass" , last_name="anass" , privilege="genin")
savingAdmin_handler.handle(admin=def_admin)