from bombcrypto.BombCryptoBot import BombCryptoBot
from modules.ImageProvider import ImageProvider


def run():
    # image_provider = ImageProvider('./bombcrypto/test-images', ['connect-wallet', 'heroes-list-1'])
    image_provider = ImageProvider()

    bomb_crypto_engine = BombCryptoBot(image_provider, debug=True)

    while True:
        bomb_crypto_engine.run()


if __name__ == '__main__':
    run()
