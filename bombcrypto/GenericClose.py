from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutionResult import MethodExecutionResultFactory, MethodExecutionResult


class GenericClose:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.has_close_button(image):
            return MethodExecutionResultFactory.not_executed()

        return self._action_executor.close_pop_up_on_game_play_screen()
