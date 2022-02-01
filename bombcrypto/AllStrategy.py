from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutionResult import MethodExecutionResult, MethodExecutionResultFactory


class AllStrategy:
    def __init__(self,
                 bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.is_in_the_heroes_screen(image):
            return MethodExecutionResultFactory.not_executed()

        if self._action_executor.send_all_heroes_to_work().is_success():
            if self._action_executor.close_pop_up_on_game_play_screen().is_success():
                return self._action_executor.return_heroes_to_work()

        return MethodExecutionResultFactory.unknown()
