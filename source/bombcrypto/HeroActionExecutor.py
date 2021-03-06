import logging

from source.bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from source.bombcrypto.Hero import Hero
from source.bombcrypto.HeroReader import HeroReader


class HeroActionExecutor:
    def __init__(self, hero_reader: HeroReader,
                 action_executor: BombCryptoActionExecutor):
        self._logger = logging.getLogger(type(self).__name__)
        self._action_executor = action_executor
        self._hero_reader = hero_reader
        self._send_to_work_attempts = 0
        self._max_send_to_work_attempts = 2

    def send_to_work(self, hero: Hero):
        if not hero.is_resting:
            return

        self._logger.info('Send searched_hero ID:' + hero.id + ' | EL:' + str(hero.energy_level) + ' to work')

        searched_hero = self._hero_reader.find_hero(hero.id_image)

        if searched_hero is None:
            self._logger.info('Hero ID:' + hero.id + ' | EL:' + str(hero.energy_level) + ' not found')

            if self._send_to_work_attempts < self._max_send_to_work_attempts:
                self._send_to_work_attempts += 1
                self.send_to_work(hero)
                return

        self._send_to_work_attempts = 0

        if searched_hero is not None:
            self._action_executor.click(searched_hero.work_rectangle().random_point())
