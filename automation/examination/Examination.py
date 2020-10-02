# region import libraries

from .TestResult import TestResult
from .TestResultList import TestResultList
from ..Test import Test
from ..rs485 import ResultValue

from time import sleep
from datetime import datetime

# endregion


class Examination(object):
    def __init__(self, automation):
        self.automation = automation
        self._initialize_test_list()

    def __getitem__(self, item_name):
        if item_name in self.__dict__:
            return self.__dict__[item_name]
        return None

    def _initialize_test_list(self):
        for x in Test.query.all():
            self.__dict__[x.name] = x

    def start_test(self, test_name):
        test_result = TestResultList()
        if test_name not in [x.name for x in self._get_selected_module_test_list]:
            return test_result

        test_result + getattr(self, "_{}_test".format(self[test_name].name))(self[test_name])

        print("[{}] Result:\n{}".format(datetime.now(), test_result))
        return test_result

    def _wait_until_stable(
            self,
            result,
            position,
            min_value,
            max_value,
            cycle_amout=20,
            timeout=0.1,
            command_line=None):

        if command_line:
            self._execute_command(command_line)
        for _ in range(cycle_amout):
            if min_value <= result[position] <= max_value:
                break
            sleep(0.1)
        sleep(timeout)
        return result[position]

    def _execute_command(self, command_line):
        self.automation.execute_command(command_line)

    def _tc_cycle(self, test):
        test_result = TestResult(test.text)

        result_instance = self.automation.module_result

        for outer_cycle in range(test.count):
            test_result.new_test()
            self._wait_until_stable(
                result_instance,
                test.start_position + outer_cycle * 2,
                test.min_value,
                test.max_value,
                command_line="{} 1 1".format(test.command),
            )
            for inner_cycle in range(test.count):
                value = result_instance[test.start_position + inner_cycle * 2]
                if inner_cycle == outer_cycle:
                    test_result.add_result(value, test.min_value < value < test.max_value)
                else:
                    test_result.add_result(value, 0 < value < test.none_value)

            self._wait_until_stable(
                result_instance,
                test.start_position + outer_cycle * 2,
                0,
                test.none_value,
                command_line="{} 1".format(test.command),
            )

        return test_result

    # region Tests

    def _din_test(self, test):
        return self._tc_cycle(test)

    def _kf_test(self, test):
        return self._tc_cycle(test)

    def _tc_test(self, test):
        return self._tc_cycle(test)

    def _exchange_test(self, test):
        test_result = TestResult(test.text)

        count = 0
        for port in self.automation.get_module_ports:
            if port.exchange < 10:
                test_result.new_test("Port {}".format(chr(ord("A") + count)))
                count += 1
                test_result.add_result("OK")

        for x in range(test.count - count):
            test_result.new_test("Port {}".format(chr(ord("A") + count + x)))
            test_result.add_result("Not OK", False)

        return test_result

    def _power_test(self, test):
        test_result = TestResult(test.text)

        result_instance = self.automation.module_result

        for x in range(2, 5):
            self._execute_command("power {}".format(x))

        for outer_cycle in range(test.count):
            self._execute_command("power {} 1 1".format(outer_cycle + 1))
            self._execute_command("power {} 1 0 1".format(outer_cycle))
            test_result.new_test()

            for inner_cycle in range(test.count):
                value = result_instance[test.start_position + inner_cycle * 2]
                if inner_cycle == outer_cycle:
                    test_result.add_result(value, test.min_value < value < test.max_value)
                else:
                    test_result.add_result(value, 0 < value < test.none_value)

        for x in range(test.count):
            self._execute_command("power {} 1".format(x + 1))

        return test_result

    def _tc12v_test(self, test):
        test_result = TestResult(test.text)

        result_instance = self.automation["mtu5"].result if self.automation["mtu5"] else ResultValue()

        for inner_cycle in range(test.count):
            value = result_instance[test.start_position + inner_cycle * 2]
            test_result.new_test()
            test_result.add_result(value, test.min_value < value < test.max_value)

        return test_result

    def _temperature_test(self, test):
        test_result = TestResult(test.text)

        result_instance = self.automation.module_result

        value = result_instance[test.start_position]
        test_result.new_test()
        test_result.add_result(value, test.min_value < value < test.max_value)

        return test_result

    # endregion

    @property
    def _get_selected_module_test_list(self):
        return list(self.automation.module.tests)
