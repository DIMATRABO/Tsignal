from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as Order_repo
from use_cases.dashboard.getUserHomeData import GetUserHomeData
from flask import Response , Blueprint 
from flask_jwt_extended import   jwt_required ,get_jwt
import json
from controllers.decorations.checkAdminPermissions import check_admin_permission


DashboardController = Blueprint("DashboardController", __name__)
order_repo = Order_repo()
userDashboard_handler = GetUserHomeData(order_repo)


@DashboardController.route('/home', methods=['GET'])
@jwt_required()
def getUserHomeData():
    try:
        userId = get_jwt()["userId"]
        data = userDashboard_handler.handle(user_id=userId)
        json_data = json.dumps(data.to_dict())
        return Response(json_data ,  status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



"""@DashboardController.route('/strategy/<strategyId>', methods=['GET'])
@jwt_required()
def getUserHomeData():
    try:
        userId = get_jwt()["userId"]
        data = userStrategyDashboard_handler.handle(user_id=userId)
        json_data = json.dumps(data.to_dict())
        return Response(json_data ,  status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


"""