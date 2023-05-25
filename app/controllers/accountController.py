from flask import Blueprint , request
from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo
from use_cases.account.save import Save
from use_cases.account.delete import Delete
from use_cases.account.getOne import GetOne
from use_cases.account.getAll import GetAll

from use_cases.account.inputs.getOneInput import GetOneInput
from use_cases.account.inputs.getAllInput import GetAllInput
from use_cases.account.getBalance import GetBalance

from gate_ways.log import Log
from forms.account.saveAccountForm import SaveAccountForm
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt
from models.model import Account
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission


AccountController = Blueprint("AccountController", __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
saving_handler = Save(postgres_repo)
delete_handler = Delete(postgres_repo)
getOne = GetOne(postgres_repo)
getAll = GetAll(postgres_repo)
getBalance_handler = GetBalance(postgres_repo)


@AccountController.route('/<accountId>', methods=['GET'])
@jwt_required()
@check_admin_permission("genin")
def getAccountById(accountId):
    try:
        account = Account()
        account = getOne.handle(getAccountInput=GetOneInput(id=accountId))
        if(account is None):
            json_data = json.dumps({"status_message":"no account found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(account.to_dict()) , status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@AccountController.route('/me', methods=['GET'])
@jwt_required()
def getAccountsByUserId():
    try:
        userId = get_jwt()["userId"]
        accounts = getAll.handle(getAccountsInput=GetAllInput(user_id=userId))
        json_data = json.dumps([account.to_dict() for account in accounts] )
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@AccountController.route('/balance/<accountId>/<currency>', methods=['GET'])
@jwt_required()
def getBalance(accountId, currency):
    try:
        userId = get_jwt()["userId"]
        balance = getBalance_handler.handle(user_id=userId , account_id=accountId , currency=currency)
        json_data = json.dumps({
            "account_id":accountId,
            "balance":balance,
            "currency":currency
        })
        return Response(json_data, status = 200, mimetype='application/json')
      
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@AccountController.route('/', methods=['POST'])
@jwt_required()
def save():
    try:
        account_json = request.get_json()
        form = SaveAccountForm(account_json)

        account = form.to_domain()
  
        logger.log("saving Account ")
        userId = get_jwt()["userId"]
        account_saved = saving_handler.handle(account=account , user_id=userId)
        json_data = json.dumps(account_saved.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@AccountController.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        delete_handler.handle(account= Account(id=id))
        status_message = "Account deleted successfully"
        logger.log(status_message)
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=200, mimetype='application/json')

    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


    


