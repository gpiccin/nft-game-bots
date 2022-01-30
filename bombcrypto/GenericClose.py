from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class GenericClose:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        close = self._image_processor.close(image)

        if not close:
            return False

        MethodExecutor.execute(self.close,
                               [image],
                               self._image_processor.is_in_the_game_play_screen,
                               [self._image_processor.game_screenshot])

        return True

    def close(self, image):
        close = self._image_processor.close(image)

        if close:
            self._action_executor.click(close.single_random_point())