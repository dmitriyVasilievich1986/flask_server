import json


class Model(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.names = [x for x in self.db._get_relate_names if x != "id"]

    def __str__(self):
        if "id" not in self.__dict__.keys():
            return self.__repr__()
        new_dict = self.db.get_table(limit=None, id=self.id)[0].values()[0]
        return json.dumps(new_dict)

    def get_object(self, *args, **kwargs):
        data = self.db.get_table(limit=None, **kwargs)[0]
        if len(data):
            data = data.values()[0][0]
            self.__init__(**data)
            return True
        return False

    def get_table(self, limit=None, *args, **kwargs):
        return self.db.get_table(limit, **kwargs)

    def delete_object(self, *args, **kwargs):
        response = self.db.delete_object(**kwargs)
        return response

    def save(self):
        new_dict = {
            key: self.__dict__[key] if key in self.__dict__ else None for key in self.names
        }
        if "id" in self.__dict__:
            message, result = self.db.update_data(self.id, **self._get_dict)
        else:
            message, result = self.db.create_new_object(**new_dict)

        if result:
            self.get_object(name=self.name)
        return message, result

    @property
    def _get_dict(self):
        return {key: self.__dict__[key] for key in self.names}
