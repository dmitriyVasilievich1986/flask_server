from flask import Blueprint, request
from ..application.database import db
from .automation import Automation

import json

automation_api = Blueprint("automation_api", __name__)
automation = Automation()


@automation_api.route("/module", methods=["GET", "POST"])
def module_view():
    if request.method == "GET":
        return str(automation)
    elif request.method == "POST":
        data = request.get_json()
        if "name" not in data:
            return "Bad request data.", 400
        message = automation.change_module(data["name"])
        response = {
            "message": message,
            "response": json.loads(str(automation))
        }
        return json.dumps(response), 200


@automation_api.route("/command", methods=["POST"])
def command_view():
    data = request.get_json()
    if "command" not in data:
        return "Bad request data.", 400
    message = automation.execute_command(data["command"])

    response = {
        "message": message
    }

    return json.dumps(response), 200
