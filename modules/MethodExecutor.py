import logging
import time

from modules.TimeControl import TimeControl


class MethodExecutor:
    SUCCESS = 1
    FAIL = 2

    @staticmethod
    def execute(method, method_arguments, check_method, check_arguments,
                max_attempts=2, seconds_waiting=4):

        attempts = 0
        timer = TimeControl(seconds_waiting)
        logger = logging.getLogger(__name__)

        for n in range(max_attempts):

            logger.debug('Execute method ' + str(method) + ' attempt ' + str(n))

            attempts += 1
            MethodExecutor._execute_method(method, method_arguments)

            timer.start()
            while not timer.is_expired():
                time.sleep(0.5)
                confirmed = MethodExecutor._execute_method(check_method, check_arguments)
                logger.debug('Execute check method ' + str(check_method) + ' returned ' + confirmed)

                if confirmed:
                    return MethodExecutor.SUCCESS

        return MethodExecutor.FAIL

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
