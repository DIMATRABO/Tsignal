from flask import Blueprint , request

from gate_ways.strategy.sqlalchimyRepo import SqlAlchimy_repo
from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as Account_repo
from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as Order_repo

from use_cases.strategy.save import Save
from use_cases.strategy.delete import Delete
from use_cases.strategy.getOne import GetOne
from use_cases.strategy.getAll import GetAll
from use_cases.strategy.getAllAdvanced import GetAllAdvanced

from use_cases.strategy.inputs.getOneInput import GetOneInput
from use_cases.strategy.inputs.getAllInput import GetAllInput
from gate_ways.log import Log

from forms.strategy.createStrategyForm import CreateStrategyForm
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt
from models.model import Strategy
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission


StrategyController = Blueprint("StrategyController", __name__)

logger = Log()
strategy_repo = SqlAlchimy_repo()
account_repo = Account_repo()
order_repo = Order_repo()

saving_handler = Save(strategy_repo)
delete_handler = Delete(strategy_repo)
getOne = GetOne(strategy_repo)
getAll = GetAll(strategy_repo)
getAllAdvanced = GetAllAdvanced(strategy_repo, account_repo,order_repo)



@StrategyController.route('/<strategyId>', methods=['GET'])
@jwt_required()
@check_admin_permission('genin')
def getStrategyById(strategyId):
    try:
        strategy = Strategy()
        strategy = getOne.handle(getStrategyInput=GetOneInput(id=strategyId))
        if(strategy is None):
            json_data = json.dumps({"status_message":"no strategy found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(strategy.to_dict()) , status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@StrategyController.route('/me/<strategyId>', methods=['GET'])
@jwt_required()
def getMyStrategyById(strategyId):
    try:
        userId = get_jwt()["userId"]
        strategy = getOne.handle(getStrategyInput=GetOneInput(id=strategyId , user_id=userId))
        if(strategy is None):
            json_data = json.dumps({"status_message":"no strategy found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(strategy.to_dict()) , status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@StrategyController.route('/me', methods=['GET'])
@jwt_required()
def getAccountsByUserId():
    try:
        userId = get_jwt()["userId"]
        strategies = getAll.handle(getStrategiesInput=GetAllInput(user_id=userId))
        json_data = json.dumps([strategy.to_dict() for strategy in strategies] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@StrategyController.route('/advanced/me', methods=['GET'])
@jwt_required()
def getStrategiesByUserId():
    try:
        userId = get_jwt()["userId"]
        strategies = getAllAdvanced.handle(user_id=userId)
        raise Exception([strategy.to_dict(strategy) for strategy in strategies])
        json_data = json.dumps([strategy.to_dict() for strategy in strategies] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@StrategyController.route('/account/<accountId>', methods=['GET'])
@jwt_required()
def getStrategiesByAccountId(accountId):
    try:
        strategies = getAll.handle(getStrategiesInput=GetAllInput(account_id=accountId))
        json_data = json.dumps([strategy.to_dict() for strategy in strategies] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')




@StrategyController.route('/', methods=['POST'])
@jwt_required()
def save():
    try:
        strategy_json = request.get_json()
        form = CreateStrategyForm(strategy_json)

        strategy = form.to_domain()
  
        logger.log("saving Strategy ")
       
        strategy_saved = saving_handler.handle(strategy=strategy)
        json_data = json.dumps(strategy_saved.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@StrategyController.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        delete_handler.handle(strategy= Strategy(id=id))
        status_message = "Strategy deleted successfully"
        logger.log(status_message)
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=200, mimetype='application/json')

    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


    


