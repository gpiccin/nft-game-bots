from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.bombcrypto.ConnectWallet import ConnectWallet
from src.bombcrypto.GoToHeroes import GoToHeroes
from src.bombcrypto.TreasureHunt import TreasureHunt
from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoBehaviours import ConnectWalletClick


class BombCryptoBot:
    def __init__(self, image_provider: ImageProvider):
        self._image_provider = image_provider
        self._bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider)
        self._connect_wallet = ConnectWallet(self._bomb_crypto_image_processor)
        self._treasure_hunt = TreasureHunt(self._bomb_crypto_image_processor)
        self._go_to_heroes = GoToHeroes(self._bomb_crypto_image_processor)

    def run(self):
        image = self._bomb_crypto_image_processor.image()

        self._connect_wallet.run(image)
        self._treasure_hunt.run(image)
        self._go_to_heroes.run(image)
