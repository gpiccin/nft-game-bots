from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor
from modules.TimeControl import TimeControl


class UnlockHeroes:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._time_to_check_heroes = TimeControl(60 * 5)
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._time_to_check_heroes.is_expired():
            return False

        back = self._image_processor.back(image)

        if not back:
            return False

        execution_result = MethodExecutor.execute(self.go_to_back,
                                                  [image],
                                                  self._image_processor.is_treasure_hunt_screen,
                                                  [self._image_processor.image])

        if execution_result == MethodExecutor.SUCCESS:
            self._time_to_check_heroes.start()

        return True

    def go_to_back(self, image):
        back = self._image_processor.back(image)

        if back:
            ActionExecutor.click(back.single_random_point())
