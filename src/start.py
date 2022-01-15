from bombcrypto.BombCryptoBot import BombCryptoBot
from modules.ImageProvider import ImageProvider


def run():
    # image_provider = ImageProvider('./bombcrypto/test-images', ['connect-wallet', 'heroes-list-1'])
    image_provider = ImageProvider()

    bot = BombCryptoBot(image_provider)
    # return debug(bot)
    loop(bot)


def loop(bot: BombCryptoBot):
    while True:
        bot.run()


def debug(bot: BombCryptoBot):
    bot._bomb_crypto_image_processor.debug()


if __name__ == '__main__':
    run()
