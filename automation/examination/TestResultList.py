from .TestResult import TestResult
from ..supportClass import BColors

from datetime import datetime


class TestResultList(object):
    def __init__(self):
        self.is_good = True
        self.list_of_test_result = list()
        self.started_at = datetime.now()

    def __add__(self, value):
        self.list_of_test_result.append(value)
        if not value.is_good:
            self.is_good = False

    def __str__(self):
        return "{}TestResultList instance. List:{}\n{}".format(
            BColors.OKGREEN if self.is_good else BColors.FAIL,
            BColors.ENDC,
            self.list_of_test_result,
        )

    def __repr__(self):
        return str(self)

    @property
    def _get_max_length_test(self):
        return max(x.get_test_length for x in self.list_of_test_result)

    @property
    def get_serialized_result(self):
        serialized_data = {
            "is_good": self.is_good,
            "started_at": self.started_at,
            "length": self._get_max_length_test,
            "result": [x.get_serialized_result for x in self.list_of_test_result],
        }
        return serialized_data
