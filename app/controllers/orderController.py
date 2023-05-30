from flask import Blueprint
from json import dumps
from flask import Response , request

from forms.order.createOrder import CreateOrderForm

from use_cases.order.inputs.getAllInput import GetAllInput
from use_cases.order.getDetails import GetDetails
from use_cases.order.create import Create
from use_cases.order.getAll import GetAll


from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as AccountRepo
from gate_ways.strategy.sqlalchimyRepo import SqlAlchimy_repo as StrategyRepo
from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as OrderRepo
from gate_ways.log import Log
from flask_jwt_extended import jwt_required, get_jwt

from controllers.decorations.checkAdminPermissions import check_admin_permission


OrderController = Blueprint('OrderController', __name__)

logger = Log()
orderRepo = OrderRepo()
accountRepo = AccountRepo()
strategyRepo = StrategyRepo()
create_handler = Create(orderRepo = orderRepo , accountRepo=accountRepo , strategyRepo=strategyRepo)
getOderDetails_handler = GetDetails(order_repo=orderRepo , accountRepo=accountRepo , strategyRepo=strategyRepo)
getOrders_handler = GetAll(repo=orderRepo)

@OrderController.route('/<webhookid>', methods=['POST'])
def create(webhookid):
    try:
        order_json = request.get_json()
        form = CreateOrderForm(order_json)
        order = form.to_domain()
        order.strategy_id=webhookid
        logger.log("new order on strategy :"+webhookid)
        json_data = dumps(create_handler.handle(order=order , key=form.key))
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@OrderController.route('/strategy/<webhookid>', methods=['GET'])
@jwt_required()
@check_admin_permission('genin')
def strategyOrders(webhookid):
    try:
        orders = getOrders_handler.handle(getOrdersInput=GetAllInput(webhook_id=webhookid))
        json_data = dumps([order.to_dict() for order in orders] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@OrderController.route('/me/strategy/<webhookid>', methods=['GET'])
@jwt_required()
def myStrategyOrders(webhookid):
    try:
        userId = get_jwt()["userId"]
        orders = getOrders_handler.handle(getOrdersInput=GetAllInput(webhook_id=webhookid , user_id=userId))
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

