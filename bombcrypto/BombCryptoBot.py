import time

from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.ConnectWallet import ConnectWallet
from bombcrypto.GenericOk import GenericOk
from bombcrypto.SendHeroesToWork import SendHeroesToWork
from bombcrypto.GreenBarStrategy import GreenBarStrategy
from bombcrypto.Hero import HeroesReader
from bombcrypto.TreasureHunt import TreasureHunt
from bombcrypto.UnlockHeroes import UnlockHeroes
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider


class BombCryptoBot:
    def __init__(self, image_provider: ImageProvider, target_images_loader: ImageLoader):
        self._image_provider = image_provider
        self._bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider, target_images_loader)
        self._connect_wallet = ConnectWallet(self._bomb_crypto_image_processor)
        self._treasure_hunt = TreasureHunt(self._bomb_crypto_image_processor)
        self._go_to_heroes = SendHeroesToWork(self._bomb_crypto_image_processor)
        self._heroes_reader = HeroesReader(self._bomb_crypto_image_processor)
        self._green_bar_strategy = GreenBarStrategy(self._bomb_crypto_image_processor, self._heroes_reader)
        self._unlock_heroes = UnlockHeroes(self._bomb_crypto_image_processor)
        self._generic_ok = GenericOk(self._bomb_crypto_image_processor)

    def run(self):
        time.sleep(0.5)
        image = self._bomb_crypto_image_processor.image()

        if image is None:
            return

        if self._generic_ok.run(image):
            return

        if self._connect_wallet.run(image):
            return

        if self._treasure_hunt.run(image):
            return

        if self._go_to_heroes.run(image):
            return

        if self._green_bar_strategy.run(image):
            return

        if self._unlock_heroes.run(image):
            return
