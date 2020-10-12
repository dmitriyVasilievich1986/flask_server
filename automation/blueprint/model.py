from flask import request
import json


class API(object):
    def __init__(self, api_object):
        self.api_object = api_object

    def index(self, id_api=None):
        if id_api and not id_api.isdigit():
            return "Bad request.", 400
        if request.method == "GET":
            return self._get_api(id_api)
        elif request.method == "POST":
            return ("Bad request.", 400) if id_api else self._post_api()
        elif request.method == "PUT":
            return ("Bad request.", 400) if not id_api else self._put_api(id_api)
        elif request.method == "DELETE":
            return ("Bad request.", 400) if not id_api else self._delete_api(id_api)
        return "Bad request.", 400

    def _get_api(self, id_api=None):
        obj = self.api_object()
        table, result, _ = obj.get_table(id=id_api) if id_api else obj.get_table()

        if not result:
            return table, 400
        return json.dumps(table), 200

    def _post_api(self):
        data = request.get_json()
        obj = self.api_object(**data)
        message, result = obj.save()

        if not result:
            return message, 400
        response = {
            "message": message,
            "response": json.loads(str(obj)),
        }

        return json.dumps(response), 201

    def _delete_api(self, id_api):
        obj = self.api_object()
        if not obj.get_object(id=id_api):
            return "Can`t delete object. Doesn`t exist."
        obj.delete_object(id=id_api)
        return "Object deleted successfuly.", 201

    def _put_api(self, id_api):
        data = request.get_json()
        obj = self.api_object()
        if not obj.get_object(id=id_api):
            return "Can`t update object. Doesn`t exist."
        for key, value in data.items():
            obj.__dict__[key] = value
        message, result = obj.save()

        if not result:
            return message, 400

        response = {
            "message": "Object updated successfuly.",
            "response": json.loads(str(obj)),
        }

        return json.dumps(response), 201
