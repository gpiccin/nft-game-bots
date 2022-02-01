from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutionResult import MethodExecutionResultFactory, MethodExecutionResult
from modules.TimeControl import TimeControl


class SendHeroesToWork:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._time_to_check_heroes = TimeControl(60 * 20)
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._time_to_check_heroes.is_expired():
            return MethodExecutionResultFactory.not_executed()

        if self._image_processor.is_in_the_heroes_screen(image):
            return MethodExecutionResultFactory.not_executed()

        if self._image_processor.is_in_the_game_play_screen(image):
            if self._action_executor.reveal_hero_icon_on_game_play_screen().is_success():
                if self._action_executor.go_to_heroes().is_success():
                    self._time_to_check_heroes.start()
                    return MethodExecutionResultFactory.success()

        if self._image_processor.has_hero_icon(image):
            if self._action_executor.go_to_heroes().is_success():
                self._time_to_check_heroes.start()
                return MethodExecutionResultFactory.success()

        return MethodExecutionResultFactory.unknown()
