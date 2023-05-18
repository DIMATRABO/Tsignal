from flask import Blueprint
from json import dumps
from flask import Response , request

from forms.order.createOrder import CreateOrderForm

from use_cases.order.inputs.getAllInput import GetAllInput
from use_cases.order.getDetails import GetDetails
from use_cases.order.create import Create
from use_cases.order.getAll import GetAll

from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo
from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as AccountRepo
from gate_ways.strategy.sqlalchimyRepo import SqlAlchimy_repo as StrategyRepo
from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as OrderRepo
from gate_ways.log import Log



OrderController = Blueprint('OrderController', __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
accountRepo = AccountRepo()
create_handler = Create(orderRepo = postgres_repo , accountRepo=accountRepo , strategyRepo=StrategyRepo())
getOrders_handler = GetAll(repo=OrderRepo())
getOderDetails_handler = GetDetails()

@OrderController.route('/<webhookid>', methods=['POST'])
def healthcheck(webhookid):
    try:
        order_json = request.get_json()
        form = CreateOrderForm(order_json)
        order = form.to_domain()
        order.strategy_id=webhookid
        logger.log("new order on strategy :"+webhookid)
        nb = create_handler.handle(order=order , key=form.key)
        json_data = dumps({"nombre_executions": nb})
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@OrderController.route('/strategy/<webhookid>', methods=['GET'])
def strategyOrders(webhookid):
    try:
        orders = getOrders_handler.handle(getOrdersInput=GetAllInput(webhook_id=webhookid))
        json_data = dumps([order.to_dict() for order in orders] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@OrderController.route('/detail/<orderId>', methods=['GET'])
def orderDetails(orderId):
    try:
        
        json_data = dumps({"msg":getOderDetails_handler.handle(order_id=orderId)})
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')

