import logging

from bombcrypto.BombCryptoBot import BombCryptoBot
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider

from core import logging_config

logging_config.setup()


def is_debug_mode():
    return False


def run():
    # image_provider = ImageProvider('./bombcrypto/test-images', ['heroes-list'])
    image_provider = ImageProvider()
    target_images_loader = ImageLoader('./bombcrypto/target-images/')

    bot = BombCryptoBot(image_provider, target_images_loader)
    # return debug(bot)
    loop(bot)


def loop(bot: BombCryptoBot):
    while True:
        try:
            bot.run()
        except Exception as e:
            logging.getLogger('start.run').error(str(e))


def debug(bot: BombCryptoBot):
    bot._bomb_crypto_image_processor.debug()


if __name__ == '__main__':
    run()
