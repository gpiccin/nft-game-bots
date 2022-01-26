from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutor import MethodExecutor
from modules.ActionExecutor import ActionExecutor


class ConnectWallet:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._image_processor.is_connect_wallet_screen(image):
            return False

        if self._image_processor.is_sign_screen(image):
            execution_result = MethodExecutor.execute(self.sign,
                                              [image],
                                              self._image_processor.is_signed,
                                              [self._image_processor.image],
                                              seconds_waiting=25)

            if execution_result == MethodExecutor.FAIL:
                ActionExecutor.refresh_page()

            return True

        execution_result = MethodExecutor.execute(self.connect,
                                          [image],
                                          self._image_processor.is_sign_screen,
                                          [self._image_processor.image],
                                          seconds_waiting=15)

        if execution_result == MethodExecutor.FAIL:
            ActionExecutor.refresh_page()

        return True

    def sign(self, image):
        sign_on_metamask_click = self._image_processor.sign_metamask(image)

        if sign_on_metamask_click:
            ActionExecutor.click(sign_on_metamask_click.first_point())

    def connect(self, image):
        connect_wallet = self._image_processor.connect_wallet(image)

        if connect_wallet:
            ActionExecutor.click(connect_wallet.first_point())
