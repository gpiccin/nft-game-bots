from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.Hero import Hero
from bombcrypto.HeroActionExecutor import HeroActionExecutor
from bombcrypto.HeroReader import HeroReader
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class GreenBarStrategy:
    def __init__(self,
                 bomb_crypto_image_processor: BombCryptoImageProcessor,
                 heroes_reader: HeroReader):
        self._hero_reader = heroes_reader
        self._image_processor = bomb_crypto_image_processor
        self._hero_height = 0
        self._last_hero_point = None
        self._first_hero_point = None
        self._heroes_analyzed = 0

    def run(self, image):
        if not self._image_processor.is_in_the_heroes_screen(image):
            return False

        heroes = self._hero_reader.load_all_heroes(image)
        reversed_heroes = heroes.reversed_heroes()

        hero_action_executor = HeroActionExecutor(self._hero_reader)

        for hero in reversed_heroes:
            if hero.energy_level != Hero.RED_ENERGY:
                hero_action_executor.send_to_work(hero)

        execution_result = MethodExecutor.execute(self.close,
                                                  [self._image_processor.image],
                                                  self._image_processor.is_in_the_game_play_screen,
                                                  [self._image_processor.image], seconds_waiting=2)

        if execution_result == MethodExecutor.SUCCESS:
            execution_result = MethodExecutor.execute(self.return_to_work,
                                                      [self._image_processor.image],
                                                      self._image_processor.is_playing,
                                                      [self._image_processor.image])

            if execution_result == MethodExecutor.FAIL:
                MethodExecutor.execute(self.go_to_back,
                                       [image],
                                       self._image_processor.is_treasure_hunt_screen,
                                       [self._image_processor.image])

        return True

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
