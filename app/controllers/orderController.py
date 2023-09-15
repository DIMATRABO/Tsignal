from flask import Blueprint
from json import dumps
from flask import Response , request

from forms.order.createOrder import CreateOrderForm
from forms.order.createBasicOrder import CreateBasicOrderForm

from use_cases.order.inputs.getAllInput import GetAllInput
from use_cases.order.getDetails import GetDetails
from use_cases.order.create import Create
from use_cases.order.createBasic import CreateBasic
from use_cases.order.createPublic import CreatePublic
from use_cases.order.getAll import GetAll
from use_cases.order.getAllPaginated import GetAllPaginated


from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as AccountRepo
from gate_ways.strategy.sqlalchimyRepo import SqlAlchimy_repo as StrategyRepo
from gate_ways.publicStrategy.sqlalchimyRepo import SqlAlchimy_repo as PublicStrategyRepo
from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as OrderRepo
from gate_ways.log import Log
from flask_jwt_extended import jwt_required, get_jwt

from controllers.decorations.checkAdminPermissions import check_admin_permission
from controllers.decorations.paginate import paginate


OrderController = Blueprint('OrderController', __name__)

logger = Log()
orderRepo = OrderRepo()
accountRepo = AccountRepo()
strategyRepo = StrategyRepo()
publicStrategyRepo = PublicStrategyRepo()
create_handler = Create(orderRepo = orderRepo , accountRepo=accountRepo , strategyRepo=strategyRepo)
create_basic_handler = CreateBasic(orderRepo = orderRepo , accountRepo=accountRepo , strategyRepo=strategyRepo)
create_public_handler = CreatePublic(orderRepo = orderRepo , accountRepo=accountRepo , publicStrategyRepo=publicStrategyRepo )
getOderDetails_handler = GetDetails(order_repo=orderRepo , strategy_repo= strategyRepo , account_repo= accountRepo)
getOrders_handler = GetAll(repo=orderRepo)
getOrdersPaginated_handler = GetAllPaginated(repo=orderRepo)


@OrderController.route('/advanced/<webhookid>', methods=['POST'])
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


@OrderController.route('/<webhookid>', methods=['POST'])
def createBasic(webhookid):
    try:
        order_json = request.get_json()
        form = CreateBasicOrderForm(order_json)
        logger.log("new basic order on strategy :"+webhookid)
        json_data = dumps(create_basic_handler.handle(order=order , key=form.key))
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')






@OrderController.route('/public/<webhookid>', methods=['POST'])
def createPublic(webhookid):
    try:
        order_json = request.get_json()
        form = CreateOrderForm(order_json)
        order = form.to_domain()
        order.strategy_id=webhookid
        logger.log("new order on strategy :"+webhookid)
        json_data = dumps(create_public_handler.handle(order=order , key=form.key))
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


@OrderController.route('/me', methods=['GET'])
@jwt_required()
def myOrders():
    try:
        userId = get_jwt()["userId"]
        orders = getOrders_handler.handle(getOrdersInput=GetAllInput(webhook_id=None , user_id=userId))
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






@OrderController.route('paginate/me', methods=['GET'])
@jwt_required()
@paginate
def myOrdersPaginated(page_number, page_size):
    try:
        userId = get_jwt()["userId"]
        data = getOrdersPaginated_handler.handle(getOrdersInput=GetAllInput(webhook_id=None, user_id=userId), page_number=page_number, page_size=page_size)
        json_data = dumps(data.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')


@OrderController.route('paginate/me/strategy/<webhookid>', methods=['GET'])
@jwt_required()
@paginate
def myStrategyOrdersPaginated(webhookid, page_number, page_size):
    try:
        userId = get_jwt()["userId"]
        data = getOrdersPaginated_handler.handle(getOrdersInput=GetAllInput(webhook_id=webhookid, user_id=userId), page_number=page_number, page_size=page_size)
        json_data = dumps(data.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')