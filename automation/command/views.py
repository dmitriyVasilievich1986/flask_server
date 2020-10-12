from .model import Command as api_object
from flask import Blueprint
from ..blueprint import API


command_api = Blueprint("command_api", __name__)
api = API(api_object)


@command_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
@command_api.route("/<id_api>", methods=["GET", "POST", "DELETE", "PUT"])
def index(id_api=None):
    return api.index(id_api)
