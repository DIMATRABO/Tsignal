from flask import Blueprint , request

from gate_ways.publicStrategy.sqlalchimyRepo import SqlAlchimy_repo as PublicStrategy_repo
from gate_ways.account.sqlalchimyRepo import SqlAlchimy_repo as Account_repo
from gate_ways.order.sqlalchimyRepo import SqlAlchimy_repo as Order_repo
from gate_ways.subscription.sqlalchimyRepo import SqlAlchimy_repo as Subscription_repo



from use_cases.admin.checkAdmin import CheckAdmin
from gate_ways.admin.sqlalchimyRepo import SqlAlchimy_repo as AdminRepo

from use_cases.publicStrategy.save import Save
from use_cases.publicStrategy.delete import Delete
from use_cases.publicStrategy.getOne import GetOne
from use_cases.publicStrategy.getAll import GetAll
from use_cases.publicStrategy.getAllAdvanced import GetAllAdvanced
from use_cases.publicStrategy.subscribe import Subscribe
from use_cases.publicStrategy.unsubscribe import Unsubscribe

from use_cases.publicStrategy.inputs.getOneInput import GetOneInput
from use_cases.publicStrategy.inputs.getAllInput import GetAllInput
from gate_ways.log import Log

from forms.publicStrategy.createPublicStrategyForm import CreatePublicStrategyForm
from forms.publicStrategy.SubscribeToPublicStrategyForm import SubscribeToPublicStrategyForm
from forms.publicStrategy.UnsubscribeToPublicStrategyForm import UnsubscribeToPublicStrategyForm

from flask import Response
from flask_jwt_extended import jwt_required, get_jwt
from models.model import PublicStrategy
import json

from controllers.decorations.checkAdminPermissions import check_admin_permission
from controllers.decorations.paginate import paginate

PublicStrategyController = Blueprint("PublicStrategyController", __name__)

logger = Log()
publicStrategy_repo = PublicStrategy_repo()
account_repo = Account_repo()
order_repo = Order_repo()
subscription_repo = Subscription_repo()
admin_repo = AdminRepo()

saving_handler = Save(publicStrategy_repo)
delete_handler = Delete(publicStrategy_repo)
getOne = GetOne(publicStrategy_repo)
getAll = GetAll(publicStrategy_repo)
getAllAdvanced = GetAllAdvanced(publicStrategy_repo, account_repo,order_repo)
subscribe_handler = Subscribe(subscription_repo, publicStrategy_repo , account_repo)
unsubscribe_handler = Unsubscribe(subscription_repo, publicStrategy_repo , account_repo)
checkAdmin = CheckAdmin(admin_repo)


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



@PublicStrategyController.route('/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe():
    try:
        userId = get_jwt()["userId"]
        publicStrategy_json = request.get_json()
        form = UnsubscribeToPublicStrategyForm(publicStrategy_json)
        subscription = form.to_domain()
        subscription.user_id = userId
        logger.log(f'user id = {userId} subscribed to PublicStrategy id = {form.strategy_id}')
        json_data = json.dumps({"status_message":unsubscribe_handler.handle(subscription).to_dict()})
        return Response(json_data , status=200, mimetype='application/json')
    
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')




@PublicStrategyController.route('', methods=['GET'])
@jwt_required()
@paginate
def getAllPaginated(page_number, page_size):
    try:
        if checkAdmin.handle(get_jwt()["adminId"], get_jwt()["login"], get_jwt()["privilege"], "genin"):
            publicStrategiesPaginated = getAll.handle(GetAllInput(all="all_admin"), page_number, page_size)
            json_data = json.dumps(publicStrategiesPaginated.to_dict())
            return Response(json_data, status=200, mimetype='application/json')
    except:
        pass

    try:
        publicStrategiesPaginated = getAll.handle(GetAllInput(all="all"), page_number, page_size)
        json_data = json.dumps(publicStrategiesPaginated.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')




@PublicStrategyController.route('/subscribed', methods=['GET'])
@jwt_required()
@paginate
def getMySubscriptionsPaginated(page_number, page_size):
    try:
        userId = get_jwt()["userId"]
        publicStrategiesPaginated = getAll.handle(GetAllInput(user_id=userId), page_number, page_size)
        json_data = json.dumps(publicStrategiesPaginated.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')


@PublicStrategyController.route('/subscribed/<account_id>', methods=['GET'])
@jwt_required()
@paginate
def getSubscribedPaginated(account_id, page_number, page_size):
    try:
        publicStrategiesPaginated = getAll.handle(GetAllInput(account_id=account_id), page_number, page_size)
        json_data = json.dumps(publicStrategiesPaginated.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')


@PublicStrategyController.route('/not-subscribed', methods=['GET'])
@jwt_required()
@paginate
def getNotSubscriptionsPaginated(page_number, page_size):
    try:
        userId = get_jwt()["userId"]
        publicStrategiesPaginated = getAll.handle(GetAllInput(not_user_id=userId), page_number, page_size)
        json_data = json.dumps(publicStrategiesPaginated.to_dict())
        return Response(json_data, status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')


@PublicStrategyController.route('/<strategy_id>', methods=['DELETE'])
@jwt_required()
@check_admin_permission('genin')
def delete(strategy_id):
    try:
        delete_handler.handle(strategy= PublicStrategy(id=strategy_id))
        status_message = "Strategy deleted successfully"
        logger.log(status_message)
        json_data = json.dumps({"status_message":status_message})
        return  Response(json_data , status=200, mimetype='application/json')

    except Exception as e:
        json_data = json.dumps({"status_message": str(e)})
        return Response(json_data, status=400, mimetype='application/json')

