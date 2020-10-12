from flask import Flask
from .configuration import ConfigurationDevelopment


def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigurationDevelopment)
    return app


def init_blueprints():
    from ..modules import module_api
    from ..command import command_api
    from ..rs485 import rs485_api
    from ..Test import test_api

    app = create_app()
    app.register_blueprint(test_api, url_prefix="/api/test")
    app.register_blueprint(rs485_api, url_prefix="/api/rs485")
    app.register_blueprint(module_api, url_prefix="/api/module")
    app.register_blueprint(command_api, url_prefix="/api/command")
    return app
