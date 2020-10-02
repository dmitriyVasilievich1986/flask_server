from ..application.database import db

import json


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    text = db.Column(db.String(50), nullable=False)
    command = db.Column(db.String(50), nullable=False)

    min_position = db.Column(db.Integer, nullable=False)
    max_position = db.Column(db.Integer, nullable=False)
    change_position = db.Column(db.Integer, nullable=False, default=3)
    change_index = db.Column(db.String(50), nullable=False, default="[5]")

    type_of_command = db.Column(db.String(50), default="")
    rs485 = db.Column(db.String(50), nullable=False)
    interrupt_data = db.Column(db.String(200), nullable=False, default="[]")

    def __init__(
        self,
        name=None,
        text=None,
        command=None,
        min_position=None,
        max_position=None,
        rs485=None,
        change_index=None,
        change_position=None,
        interrupt_data=None,
        type_of_command=None,
        * args,
        **kwargs
    ):

        self.name = name or self.name
        self.text = text or self.text
        self.command = command or self.command
        self.min_position = min_position or self.min_position
        self.max_position = max_position or self.max_position
        self.rs485 = rs485 or self.rs485
        self.type_of_command = type_of_command or self.type_of_command
        self.change_position = change_position or self.change_position

        if change_index:
            self.change_index = (
                change_index
                if isinstance(change_index, str) or isinstance(change_index, unicode)
                else json.dumps(change_index)
            )
        else:
            self.change_index = self.change_index

        if interrupt_data:
            self.interrupt_data = (
                interrupt_data
                if isinstance(interrupt_data, str) or isinstance(interrupt_data, unicode)
                else json.dumps(interrupt_data)
            )
        else:
            self.interrupt_data = self.interrupt_data

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "text": self.text,
            "command": self.command,
            "min_position": self.min_position,
            "max_position": self.max_position,
            "rs485": self.rs485,
            "type_of_command": self.type_of_command,
            "change_position": self.change_position,
            "change_index": json.loads(self.change_index),
            "interrupt_data": json.loads(self.interrupt_data),
        })

    def execute_command(self, position, set_index, automation):
        module_list = automation[self.rs485]
        if not module_list:
            return "Can`t execute command. Server data failure."
        interrupt_data = self._get_interrupt_data(position, set_index)
        for module in module_list:
            try:
                module.interrupt_data = interrupt_data
            except BaseException:
                return "Can`t execute command. Server data failure."
        return "Command executed successfuly."

    def _get_interrupt_data(self, position, set_index):
        interrupt_data = [
            set_index if i in json.loads(self.change_index) else x for i, x
            in enumerate(json.loads(self.interrupt_data))
        ]
        interrupt_data[self.change_position] += position
        return interrupt_data
