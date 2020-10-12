import sqlite3
from .column import Column, Relationship
from os import path
from ..application import BASE_DIR


FILE_NAME = path.join(BASE_DIR, "automation.db")


class DataBase(object):
    def __init__(self, table_name, *args, **kwargs):
        self.table_name = table_name
        for column in args:
            self.__dict__[column.name] = column

    def get_table(self, limit=None, *args, **kwargs):
        relationship = self.get_relationship
        if relationship and len(relationship):
            join_string = ["JOIN {}".format(x.reference_table_name) for x in relationship]
            on_string = [
                "{}.{} = {}.id".format(self.table_name, x.name, x.reference_table_name)
                for x in relationship
            ]
        conditions_line = ['{}.{} = "{}"'.format(self.table_name, key, value) for key, value in kwargs.items()]
        command_line = "SELECT * FROM {} {} {} {} {} ;".format(
            self.table_name,
            " ".join(join_string) if relationship and len(relationship) else "",
            "ON {} {}".format(", ".join(on_string), "AND" if relationship and len(conditions_line) else "")
            if relationship and len(relationship) else "WHERE " if len(conditions_line) else "",
            " AND ".join(conditions_line) if len(conditions_line) else "",
            "LIMIT {}".format(limit) if limit else ""
        )
        return self._execute_command_line(command_line, fetch=True)

    def create_new_object(self, *args, **kwargs):
        command_line = "INSERT INTO {} ({}) VALUES ({});".format(
            self.table_name,
            ", ".join(x for x in kwargs.keys()),
            ", ".join("?" for x in kwargs.values())
        )
        print(command_line, kwargs.values())
        message, result, _ = self._execute_command_line(command_line, values=kwargs.values())
        message = "New object created successfuly." if result else message
        return message, result

    def delete_object(self, *args, **kwargs):
        conditions = ["{}.{}= ? ".format(self.table_name, key, value) for key, value in kwargs.items()]
        command_line = "DELETE FROM {} WHERE {};".format(
            self.table_name,
            " AND ".join(conditions)
        )
        message, result, _ = self._execute_command_line(command_line, values=kwargs.values())
        message = "Deleted successfuly." if result else message
        return message, result

    def update_data(self, object_id, *args, **kwargs):
        conditions = ["{}= ? ".format(key) for key in kwargs.keys()]
        command_line = "UPDATE {} SET {} WHERE {};".format(
            self.table_name,
            ", ".join(conditions),
            "{}.id={}".format(self.table_name, object_id)
        )
        print(kwargs.values())
        message, result, _ = self._execute_command_line(command_line, values=kwargs.values())
        message = "Updated successfuly." if result else message
        return message, result

    def _execute_command_line(self, command_line, fetch=False, values=None):
        try:
            db = sqlite3.connect(FILE_NAME)
            cursor = db.cursor()
        except BaseException:
            return "Can`t open database. Server failure.", False, None

        try:
            if values:
                cursor.execute(command_line, values)
            else:
                cursor.execute(command_line)

            if not fetch:
                return "Command executed successfuly.", True, None

            obj, names = self._get_fetch(cursor)
            return obj, True, names

        except BaseException:
            return "Can`t execute command. Bad data.", False, None
        finally:
            db.commit()
            db.close()

    def _get_fetch(self, cursor):
        obj = dict()
        names = self._get_names([x[0] for x in cursor.description])
        for result in cursor.fetchall():
            if result[0] not in obj:
                obj[result[0]] = [
                    {
                        value: result[key].encode()
                        if isinstance(result[key], unicode) else result[key]
                        for key, value in names[0].items()
                    }
                ] + [list() for _ in range(1, len(names))]

            for x in range(1, len(names)):
                obj[result[0]][x].append(
                    {
                        value: result[key].encode()
                        if isinstance(result[key], unicode) else result[key]
                        for key, value in names[x].items()
                    }
                )
        return obj, names

    def _get_names(self, names_list):
        names = [dict()]
        for i, x in enumerate(names_list):
            if i > 0 and x == "id":
                names.append(dict())
            names[-1][i] = x
        return names

    @ property
    def get_relationship(self):
        filtered_data = filter(lambda x: isinstance(x, Relationship), self.__dict__.values())
        return filtered_data if len(filtered_data) else None

    @property
    def _get_relate_names(self):
        result = self.get_table(limit=1)
        return result[2][0].values() if result[1] else result[0]
