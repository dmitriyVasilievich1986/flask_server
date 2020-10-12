from ..database import DataBase, Column, Relationship, STRING, INTEGER, Model

import json


class Command(Model):
    db = DataBase(
        "command",
        Column("name", STRING, unique=True, nullable=False),
        Column("text", STRING, nullable=False),
        Column("description", STRING),
        Column("command", STRING),
        Column("min_position", INTEGER),
        Column("max_position", INTEGER),
        Column("change_position", INTEGER),
        Column("change_index", STRING),
        Column("type_of_command", STRING),
        Column("rs485", STRING),
        Column("interrupt_data", STRING),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(**kwargs)

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
