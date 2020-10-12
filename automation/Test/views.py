from flask import Blueprint
from .model import Test as api_object
from ..blueprint import API

test_api = Blueprint("test_api", __name__)
api = API(api_object)


@test_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
@test_api.route("/<id_api>", methods=["GET", "POST", "DELETE", "PUT"])
def index(id_api=None):
    return api.index(id_api)
