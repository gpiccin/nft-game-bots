from source.bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from source.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from source.modules.MethodExecutionResult import MethodExecutionResult
from source.modules.MethodExecutionResultFactory import MethodExecutionResultFactory


class GenericClose:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.has_close_button(image):
            return MethodExecutionResultFactory.not_executed()

        return self._action_executor.close_pop_up_on_game_play_screen()
