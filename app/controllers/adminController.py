from gate_ways.admin.sqlalchimyRepo import SqlAlchimy_repo
from use_cases.admin.getOne import GetOne
from use_cases.admin.inputs.getOneInput import GetOneInput
from use_cases.admin.auth import Auth


from gate_ways.log import Log
from forms.admin.authAdminForm import AuthAdminForm

from flask import Response ,jsonify , Blueprint , request
from flask_jwt_extended import  create_access_token, create_refresh_token, jwt_required, get_jwt_identity , get_jwt

from models.model import Admin
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission



AdminController = Blueprint("AdminController", __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
getOne = GetOne(postgres_repo)
auth = Auth(postgres_repo)


@AdminController.route('/<adminId>', methods=['GET'])
@check_admin_permission("genin")
@jwt_required()
def getAdminById(adminId):
    try:
        admin = Admin()
        admin = getOne.handle(getAdminInput=GetOneInput(id=adminId))
        if(admin is None):
            json_data = json.dumps({"status_message":"no admin found"})
            return Response(json_data ,  status=400, mimetype='application/json')
        return Response( json.dumps(admin.to_dict()) , status = 200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')





@AdminController.route('/auth', methods=['POST'])
def authAdmin():
    try:
        form = AuthAdminForm(request.get_json())
        admin = auth.handle(form)
    except Exception as e:
        logger.log("exception: " + str(e))
        json_data = json.dumps({"error": str(e)})
        return Response(json_data, status=400, mimetype='application/json')

    if admin is None:
        status_message = "Bad login or password"
        logger.log(status_message + form.login)
        json_data = json.dumps({"status_message": status_message})
        return Response(json_data, status=400, mimetype='application/json')

    additional_claims = {
           "adminId": admin.id , 
            "login": admin.login,
            "privilege": admin.privilege
            }
                                    
    access_token = create_access_token(form.login, additional_claims=additional_claims)
    refresh_token = create_refresh_token(form.login , additional_claims=additional_claims)
    logger.log("Logged in as: " + form.login)
    json_data = json.dumps({"access_token": access_token, "refresh_token": refresh_token})
    return Response(json_data, status=200, mimetype='application/json')




@AdminController.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_admin = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {
           "adminId": claims['adminId'] , 
            "login":  claims['login'],
            "privilege":  claims['privilege']
            }
    new_access_token = create_access_token(identity=current_admin,additional_claims=additional_claims)
    return jsonify(access_token=new_access_token), 200




