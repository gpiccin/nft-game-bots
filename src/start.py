from bombcrypto.BombCryptoBot import BombCryptoBot
from modules.ImageProvider import ImageProvider

#image_provider = ImageProvider('./bombcrypto/test-image_names', 'connect_wallet.png')

image_provider = ImageProvider('./bombcrypto/test-images', ['heroes-list', 'heroes-list-1'])
#image_provider = ImageProvider('./bombcrypto/test-images')

bomb_crypto_engine = BombCryptoBot(image_provider)
bomb_crypto_engine.run(debug=True)