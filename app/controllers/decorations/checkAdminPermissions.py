from functools import wraps
from flask import  Response
from flask_jwt_extended import get_jwt
from use_cases.admin.checkAdmin import CheckAdmin
from gate_ways.admin.sqlalchimyRepo import SqlAlchimy_repo as AdminRepo
import json




checkAdmin = CheckAdmin(AdminRepo())

def check_admin_permission(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                if not checkAdmin.handle(get_jwt()["adminId"], get_jwt()["login"], get_jwt()["privilege"], permission):
                    json_data = json.dumps({"msg": "unauthorized"})
                    return Response(json_data, status=401, mimetype='application/json')
            except:
                json_data = json.dumps({"msg": "unauthorized"})
                return Response(json_data, status=401, mimetype='application/json')
            
            return func(*args, **kwargs)

        return decorated_function

    return decorator
