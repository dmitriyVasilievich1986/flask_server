from ..modules import Module
from ..rs485 import RS485
from ..supportClass import BColors
from ..rs485 import ResultValue
from ..parseCommand import ParseCommand

from datetime import datetime
from flask import Blueprint
import json


class Automation:
    """main class, entry point.
    """

    def __init__(self):
        """main class, entry point.
        """

        self.serial_number = 1
        self.module_result = ResultValue()
        self.change_module(Module.query.first().name)
        self._initialize_base_bayan_modules()
        self._parse_command = ParseCommand(self)

    def start(self):
        """main class, entry point.
        """

        self.serial_number = 1
        self.module_result = ResultValue()
        self.change_module(Module.query.first().name)
        self._initialize_base_bayan_modules()

    def __getitem__(self, item_name):
        item_list = []
        for key, value in self.__dict__.items():
            if item_name in key:
                item_list.append(value)
        return item_list if len(item_list) else None

    def __str__(self):
        return json.dumps({
            "name": self.module.name,
        })

    def some(self):
        Module.query.first()
        return "OK"

    def change_module(self, module_name):
        from ..modules import Module
        module = Module.query.filter_by(name=module_name)
        module = module[0] if len(list(module)) >= 1 else None

        if not module:
            return "Module {} doesn`t exist.".format(module_name)

        self.module = module
        print('{}[{}] Selected module change to "{}" successfuly.{}'.format(
            BColors.OKGREEN, datetime.now(), module.name, BColors.ENDC
        ))
        return 'Selected module change to "{}" successfuly.'.format(module.name)

    def execute_command(self, command):
        return self._parse_command.parse_command(command)

    def _initialize_base_bayan_modules(self):
        for x in RS485.query.all():
            self.__dict__[x.name] = x
            if "moduleCh" in x.name:
                x.open_port(result=self._module_result)
            else:
                x.open_port()

    @property
    def get_module_ports(self):
        return [self.__dict__[x] for x in self.__dict__.keys() if "moduleCh" in x]
