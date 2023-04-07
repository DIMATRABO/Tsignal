from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from gate_ways.config_handler import Config_handler
from controllers.userController import UserController
from controllers.accountController import AccountController
from controllers.orderController import OrderController
from controllers.healthCheckController import healthcheck_bp
from flask_cors import CORS

config = Config_handler()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config.get_jwt_secret()
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=config.get_jwt_expiration())
jwt = JWTManager(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify(error='URL Not found'), 404

app.register_blueprint(healthcheck_bp,url_prefix = "/healthcheck")
app.register_blueprint(UserController,url_prefix = "/users")
app.register_blueprint(AccountController,url_prefix = "/accounts")
app.register_blueprint(OrderController,url_prefix = "/orders")
app.register_error_handler(404, not_found)

CORS(app)

if __name__ == "__main__":
    app.run(host=config.get_app_host(), port=config.get_app_port() , debug=config.get_app_debug_mode())