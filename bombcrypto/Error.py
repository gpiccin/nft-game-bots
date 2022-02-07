from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutionResult import MethodExecutionResultFactory, MethodExecutionResult


class Error:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.is_error(image):
            return MethodExecutionResultFactory.not_executed()

        ActionExecutor.refresh_page()
        return MethodExecutionResultFactory.success()
