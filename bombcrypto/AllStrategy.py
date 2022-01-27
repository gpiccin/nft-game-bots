from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.Hero import Hero
from bombcrypto.HeroActionExecutor import HeroActionExecutor
from bombcrypto.HeroReader import HeroReader
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class AllStrategy:
    def __init__(self,
                 bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._image_processor.is_in_the_heroes_screen(image):
            return False

        execution_result = MethodExecutor.execute(self.all,
                                                  [self._image_processor.image],
                                                  self._image_processor.is_all_working,
                                                  [self._image_processor.image], seconds_waiting=5)

        if execution_result == MethodExecutor.SUCCESS:
            execution_result = MethodExecutor.execute(self.close,
                                                      [self._image_processor.image],
                                                      self._image_processor.is_in_the_game_play_screen,
                                                      [self._image_processor.image], seconds_waiting=2)

        if execution_result == MethodExecutor.SUCCESS:
            execution_result = MethodExecutor.execute(self.return_to_work,
                                                      [self._image_processor.image],
                                                      self._image_processor.is_playing,
                                                      [self._image_processor.image], seconds_waiting=2)

            if execution_result == MethodExecutor.FAIL:
                MethodExecutor.execute(self.go_to_back,
                                       [image],
                                       self._image_processor.is_treasure_hunt_screen,
                                       [self._image_processor.image])

        return True

    def all(self, image):
        all_to_work = self._image_processor.all_heroes_to_work(image)

        if all_to_work:
            ActionExecutor.click(all_to_work.first_point())

    def close(self, image):
        close = self._image_processor.close(image)

        if close:
            ActionExecutor.click(close.first_point())

    def return_to_work(self, image):
        close = self._image_processor.slide_down_to_return_to_work(image)

        if close:
            ActionExecutor.click(close.first_point())

    def go_to_back(self, image):
        back = self._image_processor.back(image)

        if back:
            ActionExecutor.click(back.first_point())
