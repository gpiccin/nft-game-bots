#38.34
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class GenericOk:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        generic_ok = self._image_processor.generic_ok(image)

        if generic_ok:
            execution_result = MethodExecutor.execute(self.generic_ok,
                                   [image],
                                   self._image_processor.is_connect_wallet_screen,
                                   [self._image_processor.image],
                                                      seconds_waiting=10)

            if execution_result == MethodExecutor.SUCCESS:
                return True
            else:
                ActionExecutor.refresh_page()

        return False

    def generic_ok(self, image):
        generic_ok = self._image_processor.generic_ok(image)

        if generic_ok:
            ActionExecutor.click(generic_ok.first_point())