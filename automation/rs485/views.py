from flask import Blueprint
from .model import RS485 as api_object
from ..blueprint import API

import json

rs485_api = Blueprint("rs485_api", __name__)
api = API(api_object)


@rs485_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
@rs485_api.route("/<id_api>", methods=["GET", "POST", "DELETE", "PUT"])
def index(id_api=None):
    return api.index(id_api)
