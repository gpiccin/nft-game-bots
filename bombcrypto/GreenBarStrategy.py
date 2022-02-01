import time

from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.Hero import Hero
from bombcrypto.HeroActionExecutor import HeroActionExecutor
from bombcrypto.HeroList import HeroList
from bombcrypto.HeroReader import HeroReader
from modules.MethodExecutionResult import MethodExecutionResult, MethodExecutionResultFactory


class GreenBarStrategy:
    def __init__(self,
                 bomb_crypto_image_processor: BombCryptoImageProcessor,
                 heroes_reader: HeroReader,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._hero_reader = heroes_reader
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.is_in_the_heroes_screen(image):
            return MethodExecutionResultFactory.not_executed()

        self._hero_reader.update_heroes_position_information(image)
        self._hero_reader.scroll_last_heroes_page()
        self.send_heroes_to_work()

        time.sleep(2)
        self._hero_reader.scroll_up_middle_heroes_list(325)
        self.send_heroes_to_work()

        time.sleep(2)
        self._hero_reader.scroll_up_heroes_list()
        self.send_heroes_to_work()

        if self._action_executor.close_pop_up_on_game_play_screen().is_success():
            return self._action_executor.return_heroes_to_work()

        return MethodExecutionResultFactory.unknown()

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
