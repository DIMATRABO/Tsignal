from gate_ways.user.sqlalchimyRepo import SqlAlchimy_repo

from use_cases.admin.checkAdmin import CheckAdmin
from gate_ways.admin.sqlalchimyRepo import SqlAlchimy_repo as AdminRepo

from use_cases.admin.getOne import GetOne as GetOneAdmin
from use_cases.admin.inputs.getOneInput import GetOneInput as GetOneAdminInput


from use_cases.user.save import Save
from use_cases.user.update import Update
from use_cases.user.activate import Activate
from use_cases.user.delete import Delete
from use_cases.user.getOne import GetOne
from use_cases.user.auth import Auth
from use_cases.user.changePassword import ChangePassword
from use_cases.user.inputs.getOneInput import GetOneInput
from use_cases.user.inputs.getAllInput import GetAllInput
from use_cases.user.getPaginated import GetPaginated 

from gate_ways.log import Log
from forms.user.authUserForm import AuthUserForm
from forms.user.saveUserForm import SaveUserForm
from forms.user.updateUserForm import UpdateUserForm
from forms.user.changePasswordForm import ChangePasswordForm
from flask import Response ,jsonify , Blueprint , request
from flask_jwt_extended import  create_access_token, create_refresh_token, jwt_required, get_jwt_identity ,get_jwt

from models.model import User
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission
from controllers.decorations.paginate import paginate


UserController = Blueprint("UserController", __name__)

logger = Log()
postgres_repo = SqlAlchimy_repo()
admin_repo = AdminRepo()
saving_handler = Save(postgres_repo)
update_handler = Update(postgres_repo)
activate_handler = Activate(postgres_repo)
delete_handler = Delete(postgres_repo)
getOne = GetOne(postgres_repo)
getOneAdmin = GetOneAdmin(admin_repo)
auth = Auth(postgres_repo)
changePassword = ChangePassword(postgres_repo)

get_users_paginated_handler = GetPaginated(postgres_repo)
checkAdmin = CheckAdmin(admin_repo)


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


@UserController.route('paginate', methods=['GET'])
@jwt_required()
@check_admin_permission("genin")
@paginate
def usersPaginated(page_number, page_size):
    try:
        data = get_users_paginated_handler.handle(GetAllInput("all"), page_number, page_size)
        json_data = json.dumps(data.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')



@UserController.route('paginate/firstname/<firstname>', methods=['GET'])
@jwt_required()
@check_admin_permission("genin")
@paginate
def usersFirstnamePaginated(firstname , page_number, page_size):
    try:
        userPage = get_users_paginated_handler.handle(GetAllInput(first_name=firstname), page_number, page_size)
        json_data = json.dumps(userPage.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')


@UserController.route('paginate/lastname/<lastname>', methods=['GET'])
@jwt_required()
@check_admin_permission("genin")
@paginate
def usersLastnamePaginated(lastname , page_number, page_size):
    try:
        data = get_users_paginated_handler.handle(GetAllInput(last_name=lastname), page_number, page_size)
        json_data = json.dumps(data.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')




@UserController.route('/me', methods=['GET'])
@jwt_required()
def getUserBycardId():
    try:
        if checkAdmin.handle(get_jwt()["adminId"], get_jwt()["login"], get_jwt()["privilege"], "genin"):
            admin = getOneAdmin.handle(getAdminInput=GetOneAdminInput(id=get_jwt()["adminId"]))
            return Response( json.dumps(admin.to_dict()) , status = 200, mimetype='application/json') 
    except:
        pass
  
    try:
            userId = get_jwt()["userId"]
            user = User()
            user = getOne.handle(getUserInput=GetOneInput(id=userId))
            if(user is None):
                json_data = json.dumps({"status_message":"no user found"})
                return Response(json_data ,  status=400, mimetype='application/json')
            return Response( json.dumps(user.to_dict()) , status = 200, mimetype='application/json')
        
    except Exception as e :
            json_data = json.dumps({"status_message":str(e)})
            return Response(json_data , status=400, mimetype='application/json')

        

@UserController.route('/', methods=['POST'])
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
    except Exception as e:
        logger.log("exception: " + str(e))
        json_data = json.dumps({"error": str(e)})
        return Response(json_data, status=400, mimetype='application/json')

    if user is None:
        status_message = "Bad email or password"
        logger.log(status_message + form.email)
        json_data = json.dumps({"status_message": status_message})
        return Response(json_data, status=400, mimetype='application/json')

    additional_claims = {"userId": user.id}
    access_token = create_access_token(form.email, additional_claims=additional_claims)
    refresh_token = create_refresh_token(form.email, additional_claims=additional_claims)
    logger.log("Logged in as: " + form.email)
    json_data = json.dumps({"access_token": access_token, "refresh_token": refresh_token})
    return Response(json_data, status=200, mimetype='application/json')




@UserController.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {
           "userId": claims['userId'] 
            }
    access_token = create_access_token(current_user, additional_claims=additional_claims)
    return jsonify(access_token=access_token), 200




@UserController.route('/<id>', methods=['DELETE'])
@jwt_required()
@check_admin_permission("genin")
def delete(id):
   
        if delete_handler.handle(user= User(id=id)):

            status_message = "User deleted successfully"
            logger.log(status_message)
            json_data = json.dumps({"status_message":status_message})
            return  Response(json_data , status=200, mimetype='application/json')

        status_message = "User deleted successfully"
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=400, mimetype='application/json')

        


@UserController.route('/', methods=['PATCH'])
@jwt_required()
@check_admin_permission("genin")
def update():    
    try:
        user_json = request.get_json()
        form = UpdateUserForm(user_json)
    except Exception as e :
        logger.log("exeption: "+str(e))
        json_data = json.dumps({"error":str(e)})
        return Response(json_data , status = 400, mimetype='application/json')
    user = form.to_domain()
    try:
        logger.log("updating User "+ user_json["first_name"] +" "+ user_json["last_name"] )
        user_updated = update_handler.handle(user=user)
        json_data = json.dumps(user_updated.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



@UserController.route('/changepassword', methods=['POST'])
@jwt_required()
def changePasswordFUNCTION():    
    try:
        password_json = request.get_json()
        form = ChangePasswordForm(password_json)
    except Exception as e :
        logger.log("exeption: "+str(e))
        json_data = json.dumps({"error":str(e)})
        return Response(json_data , status = 400, mimetype='application/json')
    
    try:
        user_updated = changePassword.handle(user_id=get_jwt()["userId"] , old_password = form.last_password , new_password=form.new_password )
        json_data = json.dumps(user_updated.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')




@UserController.route('/activate<userId>', methods=['PATCH'])
@jwt_required()
@check_admin_permission("genin")
def activate(userId):    
    try:
        user_updated = activate_handler.handle(user_id=userId)
        json_data = json.dumps(user_updated.to_dict())
        return Response(json_data , status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')
