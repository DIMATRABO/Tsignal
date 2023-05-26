from gate_ways.user.sqlalchimyRepo import SqlAlchimy_repo
from use_cases.user.save import Save
from use_cases.user.update import Update
from use_cases.user.delete import Delete
from use_cases.user.getOne import GetOne
from use_cases.user.auth import Auth
from use_cases.user.changePassword import ChangePassword
from use_cases.user.inputs.getOneInput import GetOneInput
from gate_ways.log import Log

from flask import Response ,jsonify , Blueprint , request
from flask_jwt_extended import  create_access_token, create_refresh_token, jwt_required, get_jwt_identity ,get_jwt

from models.model import User
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission


UserController = Blueprint("UserController", __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
saving_handler = Save(postgres_repo)
update_handler = Update(postgres_repo)
delete_handler = Delete(postgres_repo)
getOne = GetOne(postgres_repo)
auth = Auth(postgres_repo)
changePassword = ChangePassword(postgres_repo)



@UserController.route('/<userId>', methods=['GET'])
@jwt_required()
@check_admin_permission("genin")
def getUserById(userId):
    try:
        user = User()
        user = getOne.handle(getUserInput=GetOneInput(id=userId))
        if(user is None):
            json_data = json.dumps({"status_message":"no user found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(user.to_dict()) , status = 200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


