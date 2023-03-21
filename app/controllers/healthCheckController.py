from flask import Blueprint
from json import dumps
from flask import Response

healthcheck_bp = Blueprint('healthcheck', __name__)

@healthcheck_bp.route('/healthcheck')
def healthcheck():
    json_data = dumps({"msg":"Service is healthy"})
    return Response(json_data , status=200, mimetype='application/json')
    