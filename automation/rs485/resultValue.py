import json


class ResultValue(object):
    """simple class to store result data from received data from module.
    """

    def __init__(self):
        """simple class to store result data from received data from module.
        """

        self.indication = dict()
        self.result = dict()

    def get_result(self, position):
        """returns result from inputed position.
        Or return 0 if dosen`t exists.
        Args:
            position (int): Key position from dictionary.

        Returns:
            float: Return value from dictionary.
        """

        return self.result[position] if position in self.result else 0

    def __getitem__(self, position):
        """returns result from inputed position.
        Or return 0 if dosen`t exists.
        Args:
            position (int): Key position from dictionary.

        Returns:
            float: Return value from dictionary.
        """

        result = 0
        result = self.result[position] if position in self.result else result
        result = self.indication[position] if position in self.indication else result

        return result

    def __str__(self):
        return json.dumps({
            "indication": self.indication,
            "result": self.result,
        })
