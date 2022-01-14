from bombcrypto.BombCryptoBot import BombCryptoBot
from modules.ImageProvider import ImageProvider

image_provider = ImageProvider('./bombcrypto/test-images', 'connect_wallet.png')

bomb_crypto_engine = BombCryptoBot()
bomb_crypto_engine.run()