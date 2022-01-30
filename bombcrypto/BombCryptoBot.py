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
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider


class BombCryptoBot:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
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

        return False
