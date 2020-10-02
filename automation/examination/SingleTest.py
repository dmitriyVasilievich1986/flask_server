class SingleTest(object):
    def __init__(self, name):
        self.name = name
        self.single_test = list()

    def __add__(self, value, *args, **kwargs):
        self.single_test.append(value)

    def __str__(self):
        return 'SingleTest instance. Name: {}, Result: {}\n'.format(self.name, self.single_test)

    def __repr__(self):
        return str(self)

    @property
    def get_serialized_result(self):
        serialized_data = {
            "name": self.name,
            "result": self.single_test,
        }
        return serialized_data
