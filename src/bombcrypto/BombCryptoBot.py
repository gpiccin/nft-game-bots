from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoBehaviours import ConnectWallet


class BombCryptoBot:
    def __init__(self, image_provider: ImageProvider):
        self._bomb_crypto_engine = None
        self._image_provider = image_provider

    def run(self, debug=False):
        self._bomb_crypto_engine = BombCryptoImageProcessor(self._image_provider, debug=debug)
        actions = self._bomb_crypto_engine.actions()

