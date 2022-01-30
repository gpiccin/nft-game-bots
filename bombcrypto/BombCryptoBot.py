import sys
import time

from bombcrypto.AllStrategy import AllStrategy
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.ConnectWallet import ConnectWallet
from bombcrypto.GenericClose import GenericClose
from bombcrypto.GenericOk import GenericOk
from bombcrypto.GreenBarStrategy import GreenBarStrategy
from bombcrypto.HeroReader import HeroReader
from bombcrypto.SendHeroesToWork import SendHeroesToWork
from bombcrypto.TreasureHunt import TreasureHunt
from bombcrypto.UnlockHeroes import UnlockHeroes
from modules.ActionExecutor import ActionExecutor
from modules.Rectangle import Rectangle


class BombCryptoBot:
    def __init__(self, position: Rectangle, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self.id = 'bot:' + position.to_string()
        self.position = position
        self._bomb_crypto_image_processor = bomb_crypto_image_processor
        self._connect_wallet = ConnectWallet(self._bomb_crypto_image_processor)
        self._treasure_hunt = TreasureHunt(self._bomb_crypto_image_processor)
        self._go_to_heroes = SendHeroesToWork(self._bomb_crypto_image_processor)
        self._heroes_reader = HeroReader(self._bomb_crypto_image_processor)
        self._green_bar_strategy = GreenBarStrategy(self._bomb_crypto_image_processor, self._heroes_reader)
        self._all_strategy = AllStrategy(self._bomb_crypto_image_processor)
        self._unlock_heroes = UnlockHeroes(self._bomb_crypto_image_processor)
        self._generic_ok = GenericOk(self._bomb_crypto_image_processor)
        self._generic_close = GenericClose(self._bomb_crypto_image_processor)
        self._wait_seconds_after_resize_window = 5

    def maximize_window(self):
        ActionExecutor.click(self.position.random_point())
        ActionExecutor.maximize()
        time.sleep(self._wait_seconds_after_resize_window)

    def return_window_to_default(self):
        image = self._bomb_crypto_image_processor.image()

        left_corner = self._bomb_crypto_image_processor.top_left_corner(image)

        if left_corner is None:
            return

        left_corner_rectangle = left_corner.first_rectangle()

        ActionExecutor.click(left_corner_rectangle.random_point())
        ActionExecutor.maximize()
        time.sleep(self._wait_seconds_after_resize_window)

    def run(self):
        image = self._bomb_crypto_image_processor.image()

        if image is None:
            return False

        if self._generic_ok.run(image):
            return True

        if self._connect_wallet.run(image):
            return True

        if self._treasure_hunt.run(image):
            return True

        if self._go_to_heroes.run(image):
            return True

        if self._green_bar_strategy.run(image):
            return True

        if self._unlock_heroes.run(image):
            return True

        if self._generic_close.run(image):
            return True

        sys.stdout.write('.')
        sys.stdout.flush()

        return False
