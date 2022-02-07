import time

from source.bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from source.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from source.modules.ActionExecutor import ActionExecutor
from source.modules.MethodExecutionResult import MethodExecutionResult
from source.modules.MethodExecutionResultFactory import MethodExecutionResultFactory
from source.modules.MethodExecutor import MethodExecutor
from source.modules.TimeControl import TimeControl


class Sign:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor
        self._max_seconds_waiting_loading_screen = 60
        self._seconds_waiting_to_check_treasure_hunt_screen = 0.5

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.is_connect_wallet_screen(image):
            return MethodExecutionResultFactory.not_executed()

        screenshot = self._image_processor.screenshot()

        if not self._image_processor.is_sign_screen(screenshot):
            return MethodExecutionResultFactory.not_executed()

        if self._sign(screenshot).is_success():
            if self._is_treasure_hunt_screen().is_success():
                return MethodExecutionResultFactory.success()

        ActionExecutor.refresh_page()
        return MethodExecutionResultFactory.fail()

    def _sign(self, screenshot) -> MethodExecutionResult:
        return MethodExecutor.execute(self._click_sign,
                                      [screenshot],
                                      self._image_processor.is_signed,
                                      [self._image_processor.game_screenshot],
                                      seconds_waiting=10)

    def _is_treasure_hunt_screen(self) -> MethodExecutionResult:
        time_loading_screen = TimeControl(self._max_seconds_waiting_loading_screen)
        time_loading_screen.start()

        while not time_loading_screen.is_expired():
            if self._image_processor.is_treasure_hunt_screen(self._image_processor.game_screenshot()):
                return MethodExecutionResultFactory.success()
            else:
                time.sleep(self._seconds_waiting_to_check_treasure_hunt_screen)

        return MethodExecutionResultFactory.fail()

    def _click_sign(self, screenshot):
        sign_on_metamask_click = self._image_processor.sign_metamask(screenshot)

        if sign_on_metamask_click:
            ActionExecutor.click(sign_on_metamask_click.single_random_point())
