from ..supportClass import BColors
from .SingleTest import SingleTest


class TestResult(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.is_good = True
        self.list_of_single_tests = list()

    def __str__(self):
        return '{}TestResult instance. Name: "{}", Length: {}, Result: {}\n{}\n'.format(
            BColors.OKGREEN if self.is_good else BColors.FAIL,
            self.name,
            self.get_test_length,
            BColors.ENDC,
            self.list_of_single_tests,
        )

    def __repr__(self):
        return str(self)

    def new_test(self, name=None):
        name = name or "{} {}".format(self.name, len(self.list_of_single_tests) + 1)
        self.list_of_single_tests.append(SingleTest(name))

    def add_result(self, value=0, result=True):
        if isinstance(value, float):
            value = round(value, 3)
        if not result:
            self.is_good = False
        self.list_of_single_tests[-1] + (value, result)

    @property
    def get_test_length(self):
        return (
            max(len(x.single_test) for x in self.list_of_single_tests)
            if len(self.list_of_single_tests) > 0
            else 0
        )

    @property
    def get_serialized_result(self):
        serialized_data = {
            "name": self.name,
            "is_good": self.is_good,
            "length": self.get_test_length,
            "result": [x.get_serialized_result for x in self.list_of_single_tests],
        }
        return serialized_data
