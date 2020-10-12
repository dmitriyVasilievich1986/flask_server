from flask import Blueprint
from .model import Module as api_object
from ..blueprint import API

import json

module_api = Blueprint("module_api", __name__)
api = API(api_object)


@module_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
@module_api.route("/<id_api>", methods=["GET", "POST", "DELETE", "PUT"])
def index(id_api=None):
    return api.index(id_api)
