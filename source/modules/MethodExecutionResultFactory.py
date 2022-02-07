from source.modules.MethodExecutionResult import MethodExecutionResult


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
