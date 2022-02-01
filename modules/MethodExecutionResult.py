class MethodExecutionResult:
    NOT_EXECUTED = -1
    UNKNOWN = -1
    SUCCESS = 1
    FAIL = 2

    def __init__(self, result: int = UNKNOWN):
        self.result = result

    def executed(self):
        return self.result != MethodExecutionResult.NOT_EXECUTED

    def is_success(self):
        return self.result == MethodExecutionResult.SUCCESS

    def is_failed(self):
        return self.result == MethodExecutionResult.FAIL


class MethodExecutionResultFactory:
    @staticmethod
    def not_executed():
        return MethodExecutionResult(MethodExecutionResult.NOT_EXECUTED)

    @staticmethod
    def unknown():
        return MethodExecutionResult(MethodExecutionResult.UNKNOWN)

    @staticmethod
    def success():
        return MethodExecutionResult(MethodExecutionResult.SUCCESS)

    @staticmethod
    def fail():
        return MethodExecutionResult(MethodExecutionResult.FAIL)
