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


@automation_api.route("/mtu5")
def mtu5_view():
    mtu5 = automation["mtu5"]
    if not mtu5:
        return "Bad request. Server data failure.", 400
    response = {
        "name": mtu5[0].name,
        "result": mtu5[0].result.result,
        "indication": mtu5[0].result.indication,
    }

    return json.dumps(response), 200


@automation_api.route("/ain8")
def ain8_view():
    ain8 = automation["ain8"]
    if not ain8:
        return "Bad request. Server data failure.", 400
    response = {
        "name": ain8[0].name,
        "result": ain8[0].result.result,
        "indication": ain8[0].result.indication,
    }

    return json.dumps(response), 200


@automation_api.route("/result")
def module_result_view():
    module_result = automation.module_result
    response = {
        "name": automation.module.name,
        "result": module_result.result,
        "indication": module_result.indication,
    }

    return json.dumps(response), 200


@automation_api.route("/dout_din16")
def dout_din16_view():
    dout_din16 = automation["dout_din16"]
    if not dout_din16:
        return "Bad request. Server data failure.", 400
    response = {
        "name": dout_din16[0].name,
        "result": dout_din16[0].result.result,
        "indication": dout_din16[0].result.indication,
    }

    return json.dumps(response), 200


@automation_api.route("/dout_din32")
def dout_din32_view():
    dout_din32 = automation["dout_din32"]
    if not dout_din32:
        return "Bad request. Server data failure.", 400
    response = {
        "name": dout_din32[0].name,
        "result": dout_din32[0].result.result,
        "indication": dout_din32[0].result.indication,
    }

    return json.dumps(response), 200
