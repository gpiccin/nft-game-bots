from source.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from source.modules.ActionExecutor import ActionExecutor
from source.modules.MethodExecutionResult import MethodExecutionResult
from source.modules.MethodExecutionResultFactory import MethodExecutionResultFactory


class GenericOk:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.has_ok_button(image):
            return MethodExecutionResultFactory.not_executed()

        ActionExecutor.refresh_page()
        return MethodExecutionResultFactory.success()
