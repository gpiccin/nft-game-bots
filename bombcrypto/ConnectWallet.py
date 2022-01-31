from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutor import MethodExecutor
from modules.ActionExecutor import ActionExecutor
from modules.TimeControl import TimeControl


class ConnectWallet:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._image_processor.is_connect_wallet_screen(image):
            return False

        screenshot = self._image_processor.screenshot()

        if self._image_processor.is_sign_screen(screenshot):
            execution_result = MethodExecutor.execute(self.sign,
                                                      [screenshot],
                                                      self._image_processor.is_signed,
                                                      [self._image_processor.game_screenshot],
                                                      seconds_waiting=10)

            if execution_result == MethodExecutor.FAIL:
                ActionExecutor.refresh_page()
            else:
                time_to_treasure_hunt = TimeControl(60)
                time_to_treasure_hunt.start()

                while not time_to_treasure_hunt.is_expired():
                    if self._image_processor.is_treasure_hunt_screen(self._image_processor.game_screenshot()):
                        return True

                ActionExecutor.refresh_page()

            return True

        execution_result = MethodExecutor.execute(self.connect,
                                                  [image],
                                                  self._image_processor.is_sign_screen,
                                                  [self._image_processor.screenshot],
                                                  seconds_waiting=15)

        if execution_result == MethodExecutor.FAIL:
            ActionExecutor.refresh_page()

        return True

    def sign(self, screenshot):
        sign_on_metamask_click = self._image_processor.sign_metamask(screenshot)

        if sign_on_metamask_click:
            ActionExecutor.click(sign_on_metamask_click.single_random_point())

    def connect(self, image):
        connect_wallet = self._image_processor.connect_wallet(image)

        if connect_wallet:
            self._action_executor.click(connect_wallet.single_random_point())
