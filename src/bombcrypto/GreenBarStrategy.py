from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.bombcrypto.Hero import Hero, HeroesReader
from src.logger import log
from src.modules.ActionExecutor import ActionExecutor
from src.modules.MethodExecutor import MethodExecutor


class GreenBarStrategy:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 heroes_reader: HeroesReader):
        self._heroes_header = heroes_reader
        self._image_processor = bomb_crypto_image_processor
        self._hero_height = 0
        self._last_hero_point = None
        self._first_hero_point = None
        self._heroes_analyzed = 0
        self.heroes = {}

    def run(self, image):
        if not self._image_processor.is_in_the_heroes_screen(image):
            return

        self.heroes = self._heroes_header.load_all_heroes(image)

        log(len(self.heroes))

        for hero_id in self.heroes:
            hero = self.heroes[hero_id]
            if hero.energy_level != Hero.RED_ENERGY:
                hero.send_to_work()

        execute_result = MethodExecutor.execute(self.close,
                                                [self._image_processor.image],
                                                self._image_processor.is_in_the_game_play_screen,
                                                [self._image_processor.image])

        if execute_result == MethodExecutor.SUCCESS:
            execute_result = MethodExecutor.execute(self.return_to_work,
                                                    [self._image_processor.image],
                                                    self._image_processor.is_playing,
                                                    [self._image_processor.image])

    def close(self, image):
        close = self._image_processor.close(image)

        if close:
            ActionExecutor.click(close.first_point())

    def return_to_work(self, image):
        close = self._image_processor.slide_down_to_return_to_work(image)

        if close:
            ActionExecutor.click(close.first_point())
