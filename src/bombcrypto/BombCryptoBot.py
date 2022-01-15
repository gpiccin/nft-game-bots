from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.bombcrypto.ConnectWallet import ConnectWallet
from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoBehaviours import ConnectWalletClick


class BombCryptoBot:
    def __init__(self, image_provider: ImageProvider, debug=False):
        self._image_provider = image_provider
        self._bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider, debug=debug)
        self._connect_wallet = ConnectWallet(self._bomb_crypto_image_processor)

    def run(self):
        self._connect_wallet.run()
