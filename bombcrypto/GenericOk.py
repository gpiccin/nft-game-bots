from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor


class GenericOk:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        generic_ok = self._image_processor.generic_ok(image)

        if not generic_ok:
            return False

        ActionExecutor.refresh_page()
        return True
