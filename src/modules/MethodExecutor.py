import time
from src.logger import log
from src.modules.TimeControl import TimeControl


class MethodExecutor:
    SUCCESS = 1
    FAIL = 2

    @staticmethod
    def execute(method, method_arguments, check_method=None, check_arguments=None,
                max_attempts=2, seconds_waiting=4):

        attempts = 0
        timer = TimeControl(seconds_waiting)

        for n in range(max_attempts):
            log('Execute method ' + str(method) + ' attempt ' + str(n))
            MethodExecutor._execute_method(method, method_arguments)

            if check_method:
                attempts += 1

                confirmed = False

                timer.start()
                while not timer.is_expired():
                    log('Execute check method ' + str(check_method))
                    confirmed = MethodExecutor._execute_method(check_method, check_arguments)

                    if confirmed:
                        break
                    else:
                        time.sleep(seconds_waiting / 4)

                if confirmed:
                    return MethodExecutor.SUCCESS

                if attempts > max_attempts:
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
