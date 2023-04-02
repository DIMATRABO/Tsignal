from flask import Blueprint , request
from gate_ways.user.sqlalchimyRepo import SqlAlchimy_repo
from use_cases.user.save import Save
from use_cases.user.delete import Delete
from use_cases.user.getOne import GetOne
from use_cases.user.auth import Auth
from use_cases.user.inputs.getOneInput import GetOneInput
from gate_ways.log import Log
from forms.user.authUserForm import AuthUserForm
from forms.user.saveUserForm import SaveUserForm
from flask import Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from models.model import User
import json



UserController = Blueprint("UserController", __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
saving_handler = Save(postgres_repo)
delete_handler = Delete(postgres_repo)
getOne = GetOne(postgres_repo)
auth = Auth(postgres_repo)


@UserController.route('/<userId>', methods=['GET'])
@jwt_required()
def getUserById(userId):
    try:
        user = User()
        user = getOne.handle(user , getUserInput=GetOneInput(id=userId))
        if(user is None):
            json_data = json.dumps({"status_message":"no user found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response(user.to_dict() , status = 200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')




@UserController.route('/cardid/<cardid>', methods=['GET'])
@jwt_required()
def getUserBycardId(cardid):
    try:
        user = User()
        user = getOne.handle(user , getUserInput=GetOneInput(id_card=cardid))
        if(user is None): 
            json_data = json.dumps({"status_message":"no user found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response(user.to_dict(),status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


    

@UserController.route('/', methods=['POST'])
#@jwt_required()
def save():
    try:
        user_json = request.get_json()
        form = SaveUserForm(user_json)
    except Exception as e :
        logger.log("exeption: "+str(e))
        json_data = json.dumps({"error":str(e)})
        return Response(json_data , status = 400, mimetype='application/json')
    user = form.to_domain()
    try:
        logger.log("saving User "+ user_json["first_name"] +" "+ user_json["last_name"] )
        user_saved = saving_handler.handle(user=user)
        json_data = json.dumps(user_saved.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@UserController.route('/auth', methods=['POST'])
def authUser():
    try:
        form = AuthUserForm(request.get_json())
        user = auth.handle(form)
    except Exception as e :
        logger.log("exeption: "+str(e))
        json_data = json.dumps({"error":str(e)})
        return Response(json_data , status = 400, mimetype='application/json')

    if user is None:
        status_message = "Bad username or password "
        logger.log(status_message + form.login)
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=400, mimetype='application/json')

    additional_claims = {"userId": user.id}
    access_token = create_access_token(form.login, additional_claims=additional_claims)
    logger.log("Logged in as: "+form.login)
    return Response(access_token , status=200, mimetype='application/json')


@UserController.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        if delete_handler.handle(user= User(id=id)):

            status_message = "User deleted successfully"
            logger.log(status_message)
            json_data = json.dumps({"status_message":status_message})
            return  Response(json_data , status=200, mimetype='application/json')

        status_message = "User deleted successfully"
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=400, mimetype='application/json')
        
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


        


