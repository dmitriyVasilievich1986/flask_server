from ..command import Command

from time import sleep


class ParseCommand(object):
    def __init__(self, automation=None, *args, **kwargs):
        self.automation = automation

    def parse_command(self, command_text, *args, **kwargs):
        command, position, set_index, timeout = self._get_splited_command(command_text)

        message = 'Can`t execute command: "{}". No such command.'.format(command)
        for x in Command.query.filter_by(command=command):
            message = x.execute_command(position, set_index, self.automation)
        sleep(timeout)

        return message

    def _get_splited_command(self, command_text, *args, **kwargs):
        splited_command = command_text.split()
        command = splited_command[0]
        position = int(splited_command[1]) if len(splited_command) >= 2 else 0
        set_index = 1 if len(splited_command) >= 3 and int(splited_command[2]) > 0 else 0
        timeout = float(splited_command[3]) if len(splited_command) >= 4 else 0.1

        return command, position, set_index, timeout
