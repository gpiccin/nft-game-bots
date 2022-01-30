import time
from typing import List

from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.Hero import Hero
from bombcrypto.HeroActionExecutor import HeroActionExecutor
from bombcrypto.HeroList import HeroList
from bombcrypto.HeroReader import HeroReader
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class GreenBarStrategy:
    def __init__(self,
                 bomb_crypto_image_processor: BombCryptoImageProcessor,
                 heroes_reader: HeroReader,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._hero_reader = heroes_reader
        self._image_processor = bomb_crypto_image_processor
        self._hero_height = 0
        self._last_hero_point = None
        self._first_hero_point = None
        self._heroes_analyzed = 0

    def run(self, image):
        if not self._image_processor.is_in_the_heroes_screen(image):
            return False

        self._hero_reader.update_heroes_position_information(image)
        self._hero_reader.scroll_last_heroes_page()
        self.send_heroes_to_work()

        time.sleep(2)
        self._hero_reader.scroll_up_middle_heroes_list(325)
        self.send_heroes_to_work()

        time.sleep(2)
        self._hero_reader.scroll_up_heroes_list()
        self.send_heroes_to_work()

        execution_result = MethodExecutor.execute(self.close,
                                                  [self._image_processor.game_screenshot],
                                                  self._image_processor.is_in_the_game_play_screen,
                                                  [self._image_processor.game_screenshot], seconds_waiting=2)

        if execution_result == MethodExecutor.SUCCESS:
            execution_result = MethodExecutor.execute(self.return_to_work,
                                                      [self._image_processor.game_screenshot],
                                                      self._image_processor.is_playing,
                                                      [self._image_processor.game_screenshot])

            if execution_result == MethodExecutor.FAIL:
                MethodExecutor.execute(self.go_to_back,
                                       [image],
                                       self._image_processor.is_treasure_hunt_screen,
                                       [self._image_processor.game_screenshot])

        return True

    def send_heroes_to_work(self) -> HeroList:
        while True:
            heroes = self._hero_reader.read_heroes_from_screen()
            hero_action_executor = HeroActionExecutor(self._hero_reader, self._action_executor)
            reversed_heroes = heroes.reversed_heroes()

            for hero in reversed_heroes:
                if hero.energy_level != Hero.RED_ENERGY:
                    hero_action_executor.send_to_work(hero)

            if heroes.count_of_heroes_to_work() == 0:
                break

        return heroes

    def close(self, image):
        close = self._image_processor.close(image)

        if close:
            self._action_executor.click(close.single_random_point())

    def return_to_work(self, image):
        coin = self._image_processor.coin(image)

        if coin:
            self._action_executor.click(coin.single_random_point())

    def go_to_back(self, image):
        back = self._image_processor.back(image)

        if back:
            self._action_executor.click(back.single_random_point())
