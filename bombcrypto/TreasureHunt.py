from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutionResult import MethodExecutionResultFactory, MethodExecutionResult


class TreasureHunt:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.is_treasure_hunt_screen(image):
            return MethodExecutionResultFactory.not_executed()

        return self._action_executor.go_to_treasure_hunt()
