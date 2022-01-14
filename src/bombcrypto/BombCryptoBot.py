from src.bombcrypto.BombCryptoEngine import BombCryptoEngine
from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoActions import ConnectWallet


class BombCryptoBot:
    def __init__(self):
        self._bomb_crypto_engine = None
        self._image_provider = ImageProvider('./bombcrypto/test-images', 'connect_wallet')

    def run(self, debug=False):
        self._bomb_crypto_engine = BombCryptoEngine(self._image_provider, debug=debug)
        actions = self._bomb_crypto_engine.actions()

