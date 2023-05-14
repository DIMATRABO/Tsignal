from flask import Blueprint
from json import dumps
from flask import Response , request

from forms.order.createOrder import CreateOrderForm

from use_cases.order.create import Create

from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo
from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as AccountRepo
from gate_ways.log import Log



OrderController = Blueprint('OrderController', __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
accountRepo = AccountRepo()
create_handler = Create(orderRepo = postgres_repo , accountRepo=accountRepo)


@OrderController.route('/<strategyId>', methods=['POST'])
def healthcheck(strategyId):
    try:
        order_json = request.get_json()
        form = CreateOrderForm(order_json)
        order = form.to_domain()
        order.strategy_id=strategyId
        logger.log("new order on strategy :"+strategyId)

        nb = create_handler.handle(order=order)
        json_data = dumps({"nombre_executions": nb})
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')

