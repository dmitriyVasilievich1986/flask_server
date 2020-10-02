from flask import Blueprint, request
from .model import Module as api_object
from ..application.database import db

import json

module_api = Blueprint("module_api", __name__)


@module_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
@module_api.route("/<id_api>", methods=["GET", "POST", "DELETE", "PUT"])
def index(id_api=None):
    if id_api and not id_api.isdigit():
        return "Bad request.", 400
    if request.method == "GET":
        return get_api(id_api)
    elif request.method == "POST":
        return ("Bad request.", 400) if id_api else post_api()
    elif request.method == "PUT":
        return ("Bad request.", 400) if not id_api else put_api(id_api)
    elif request.method == "DELETE":
        return ("Bad request.", 400) if not id_api else delete_api(id_api)
    return "Bad request.", 400


def get_api(id_api=None):
    if id_api:
        if not api_object.query.get(id_api):
            return "Object doesn`t exist.", 400
        return str(api_object.query.get(id_api)), 200
    else:
        obj = [json.loads(str(x)) for x in api_object.query.all()]
        return json.dumps(obj), 200


def post_api():
    data = request.get_json()
    try:
        obj = api_object(**data)
        db.session.add(obj)
        db.session.commit()
    except BaseException:
        print("NOT OK")
        return "Can`t create object. Bad data.", 400

    response = {
        "message": "Object created successfuly.",
        "response": json.loads(str(obj)),
    }

    return json.dumps(response), 201


def delete_api(id_api):
    if not api_object.query.get(id_api):
        return "Object doesn`t exist.", 400
    api_object.query.filter_by(id=id_api).delete()
    db.session.commit()

    return "Object deleted successfuly.", 201


def put_api(id_api):
    obj = api_object.query.get(id_api)
    if not obj:
        return "Object doesn`t exist.", 400
    try:
        data = request.get_json()
        obj.__init__(**data)
        db.session.add(obj)
        db.session.commit()
    except BaseException:
        return "Can`t update object. Bad data.", 400

    response = {
        "message": "Object updated successfuly.",
        "response": json.loads(str(obj)),
    }

    return json.dumps(response), 201
