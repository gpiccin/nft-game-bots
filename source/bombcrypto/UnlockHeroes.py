from source.bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from source.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from source.modules.MethodExecutionResult import MethodExecutionResult
from source.modules.MethodExecutionResultFactory import MethodExecutionResultFactory
from source.modules.TimeControl import TimeControl


class UnlockHeroes:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._time_to_check_heroes = TimeControl(60 * 5)
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._time_to_check_heroes.is_expired():
            return MethodExecutionResultFactory.not_executed()

        if not self._image_processor.is_in_the_game_play_screen(image):
            return MethodExecutionResultFactory.not_executed()

        if self._action_executor.go_back().is_success():
            if self._action_executor.go_to_treasure_hunt().is_success():
                self._time_to_check_heroes.start()
                return MethodExecutionResultFactory.success()

        return MethodExecutionResultFactory.unknown()
