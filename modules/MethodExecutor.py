import logging
import time

from modules.MethodExecutionResult import MethodExecutionResult, MethodExecutionResultFactory
from modules.TimeControl import TimeControl


class MethodExecutor:
    @staticmethod
    def execute(method, method_arguments, check_method, check_arguments,
                max_attempts=2, seconds_waiting=4) -> MethodExecutionResult:

        attempts = 0
        timer = TimeControl(seconds_waiting)
        logger = logging.getLogger(__name__)

        for n in range(max_attempts):

            logger.debug('Execute ' + MethodExecutor._get_method_name(method) + ' attempt ' + str(n))

            attempts += 1
            MethodExecutor._execute_method(method, method_arguments)

            timer.start()
            while not timer.is_expired():
                timer.wait()
                confirmed = MethodExecutor._execute_method(check_method, check_arguments)
                logger.debug('Check method ' + MethodExecutor._get_method_name(check_method) + ' = ' + str(confirmed))

                if confirmed:
                    return MethodExecutionResultFactory.success()

        return MethodExecutionResultFactory.fail()

    @staticmethod
    def _get_method_name(method):
        method_full_name = str(method)
        method_index = method_full_name.index('method ') + 7
        of_index = method_full_name.index(' of ')
        return method_full_name[method_index:of_index]

    @staticmethod
    def _execute_method(method, method_arguments):
        arguments = []

        for arg in method_arguments:
            if callable(arg):
                arguments.append(arg())
                continue

            arguments.append(arg)

        return method(*arguments)

    @staticmethod
    def execute_and_wait(method, method_arguments, seconds_to_wait=1):
        result = method(*method_arguments)

        if result:
            time.sleep(seconds_to_wait)

        return result
