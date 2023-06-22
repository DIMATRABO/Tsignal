from flask import Blueprint , request

from gate_ways.publicStrategy.sqlalchimyRepo import SqlAlchimy_repo as PublicStrategy_repo
from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as Account_repo
from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as Order_repo
from gate_ways.subscription.sqlalchimyRepo import SqlAlchimy_repo as Subscription_repo




from use_cases.publicStrategy.save import Save
from use_cases.publicStrategy.delete import Delete
from use_cases.publicStrategy.getOne import GetOne
from use_cases.publicStrategy.getAll import GetAll
from use_cases.publicStrategy.getAllAdvanced import GetAllAdvanced
from use_cases.publicStrategy.subscribe import Subscribe

from use_cases.publicStrategy.inputs.getOneInput import GetOneInput
from use_cases.publicStrategy.inputs.getAllInput import GetAllInput
from gate_ways.log import Log

from forms.publicStrategy.createPublicStrategyForm import CreatePublicStrategyForm
from forms.publicStrategy.SubscribeToPublicStrategyForm import SubscribeToPublicStrategyForm

from flask import Response
from flask_jwt_extended import jwt_required, get_jwt
from models.model import PublicStrategy
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission


PublicStrategyController = Blueprint("PublicStrategyController", __name__)

logger = Log()
publicStrategy_repo = PublicStrategy_repo()
account_repo = Account_repo()
order_repo = Order_repo()
subscription_repo = Subscription_repo()

saving_handler = Save(publicStrategy_repo)
delete_handler = Delete(publicStrategy_repo)
getOne = GetOne(publicStrategy_repo)
getAll = GetAll(publicStrategy_repo)
getAllAdvanced = GetAllAdvanced(publicStrategy_repo, account_repo,order_repo)
subscribe_handler = Subscribe(subscription_repo, publicStrategy_repo , account_repo)


@PublicStrategyController.route('/', methods=['POST'])
@jwt_required()
@check_admin_permission('genin')
def save():
    try:
        publicStrategy_json = request.get_json()
        form = CreatePublicStrategyForm(publicStrategy_json)

        publicStrategy = form.to_domain()
  
        logger.log("saving PublicStrategy ")
       
        publicStrategy_saved = saving_handler.handle(publicStrategy=publicStrategy)
        json_data = json.dumps(publicStrategy_saved.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')




@PublicStrategyController.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    try:
        userId = get_jwt()["userId"]
        publicStrategy_json = request.get_json()
        form = SubscribeToPublicStrategyForm(publicStrategy_json)
        subscription = form.to_domain()
        subscription.user_id = userId
        logger.log(f'user id = {userId} subscribed to PublicStrategy id = {form.strategy_id}')
        json_data = json.dumps({"status_message":subscribe_handler.handle(subscription).to_dict()})
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


"""

@PublicStrategyController.route('/<publicStrategyId>', methods=['GET'])
@jwt_required()
@check_admin_permission('genin')
def getPublicStrategyById(publicStrategyId):
    try:
        publicStrategy = getOne.handle(getPublicStrategyInput=GetOneInput(id=publicStrategyId))
        if(publicStrategy is None):
            json_data = json.dumps({"status_message":"no publicStrategy found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(publicStrategy.to_dict()) , status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@PublicStrategyController.route('/me/<publicStrategyId>', methods=['GET'])
@jwt_required()
def getMyPublicStrategyById(publicStrategyId):
    try:
        userId = get_jwt()["userId"]
        publicStrategy = getOne.handle(getPublicStrategyInput=GetOneInput(id=publicStrategyId , user_id=userId))
        if(publicStrategy is None):
            json_data = json.dumps({"status_message":"no publicStrategy found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(publicStrategy.to_dict()) , status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@PublicStrategyController.route('/me', methods=['GET'])
@jwt_required()
def getAccountsByUserId():
    try:
        userId = get_jwt()["userId"]
        strategies = getAll.handle(getStrategiesInput=GetAllInput(user_id=userId))
        json_data = json.dumps([publicStrategy.to_dict() for publicStrategy in strategies] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@PublicStrategyController.route('/advanced/me', methods=['GET'])
@jwt_required()
def getStrategiesByUserId():
    try:
        userId = get_jwt()["userId"]
        strategies = getAllAdvanced.handle(user_id=userId)
        json_data = json.dumps([publicStrategy.to_dict() for publicStrategy in strategies] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@PublicStrategyController.route('/account/<accountId>', methods=['GET'])
@jwt_required()
def getStrategiesByAccountId(accountId):
    try:
        strategies = getAll.handle(getStrategiesInput=GetAllInput(account_id=accountId))
        json_data = json.dumps([publicStrategy.to_dict() for publicStrategy in strategies] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')







@PublicStrategyController.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        userId = get_jwt()["userId"]
        delete_handler.handle(publicStrategy= PublicStrategy(id=id) , user_id=userId)
        status_message = "PublicStrategy deleted successfully"
        logger.log(status_message)
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=200, mimetype='application/json')

    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


    


"""