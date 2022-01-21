from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.bombcrypto.ConnectWallet import ConnectWallet
from src.bombcrypto.SendHeroesToWork import SendHeroesToWork
from src.bombcrypto.GreenBarStrategy import GreenBarStrategy
from src.bombcrypto.Hero import HeroesReader
from src.bombcrypto.TreasureHunt import TreasureHunt
from src.bombcrypto.UnlockHeroes import UnlockHeroes
from src.modules.ImageProvider import ImageProvider


class BombCryptoBot:
    def __init__(self, image_provider: ImageProvider):
        self._image_provider = image_provider
        self._bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider)

        self._connect_wallet = ConnectWallet(self._bomb_crypto_image_processor)
        self._treasure_hunt = TreasureHunt(self._bomb_crypto_image_processor)
        self._go_to_heroes = SendHeroesToWork(self._bomb_crypto_image_processor)
        self._heroes_reader = HeroesReader(self._bomb_crypto_image_processor)
        self._green_bar_strategy = GreenBarStrategy(self._bomb_crypto_image_processor, self._heroes_reader)
        self._unlock_heroes = UnlockHeroes(self._bomb_crypto_image_processor)

    def run(self):
        image = self._bomb_crypto_image_processor.image()

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
