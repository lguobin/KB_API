from flask import Flask, jsonify
from settings import config
from app.api import api_blueprint
from app.common.errors import Errors
from app.extensions import config_extentions, setup_log

# from flask import current_app
# current_app._get_current_object()

app = Flask(__name__)
Apps = app.app_context().push()



def create_app(config_name):
    # todo 启用日志功能
    Config = config[config_name]
    setup_log(Config)

    app.config.from_object(config[config_name])
    config_extentions(app)
    api_blueprint(app)
    errors(app)
    return app


def errors(app):
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    def page_not_found(e):
        return jsonify(Errors(e))

    @app.errorhandler(500)
    def server_error(e):
        return jsonify(Errors(e))
