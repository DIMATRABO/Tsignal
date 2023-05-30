from gate_ways.exchange.sqlalchimyRepo import SqlAlchimy_repo as Exchange_repo
from use_cases.exchange.getAll import GetAll
from use_cases.exchange.getSymbols import GetSymbols
from use_cases.exchange.getQuotes import GetQuotes
from use_cases.exchange.inputs.getAllInput import GetAllInput

from flask import Response , Blueprint 
from flask_jwt_extended import   jwt_required 
import json


ExchangeController = Blueprint("ExchangeController", __name__)

exchange_repo = Exchange_repo()

get_all_handler = GetAll(exchange_repo)
get_symbols_handler = GetSymbols()
get_quotes_handler = GetQuotes()


@ExchangeController.route('', methods=['GET'])
def getAll():
    try:
        data = get_all_handler.handle(GetAllInput(all="all"))
        json_data = json.dumps([ exchange.to_dict() for exchange in data])
        return Response(json_data ,  status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')


@ExchangeController.route('/symbols/<exchangeId>', methods=['GET'])
def getSymbols(exchangeId):
    try:
        data = get_symbols_handler.handle(exchangeId)
        json_data = json.dumps(data)
        return Response(json_data ,  status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')

@ExchangeController.route('/quotes/<exchangeId>', methods=['GET'])
def getQuotes(exchangeId):
    try:
        data = get_quotes_handler.handle(exchangeId)
        json_data = json.dumps(data)
        return Response(json_data ,  status=200, mimetype='application/json')
    except Exception as e :
        json_data = json.dumps({"status_message":str(e)})
        return Response(json_data , status=400, mimetype='application/json')



