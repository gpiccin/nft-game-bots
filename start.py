import logging
import sys
import time

from bombcrypto.BombCryptoBot import BombCryptoBot
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider

from core import logging_config

logging_config.setup()


def is_debug_mode():
    return False


def run():
    # image_provider = ImageProvider('./bombcrypto/test-images', ['heroes-heroes_list-2'])
    image_provider = ImageProvider()
    target_images_loader = ImageLoader('bombcrypto/target-images')
    bomb_crypto_image_processor = BombCryptoImageProcessor(image_provider, target_images_loader)

    bot = BombCryptoBot(bomb_crypto_image_processor)
    #return debug(bot)

    loop(bot)


def loop(bot: BombCryptoBot):
    while True:
        # try:
        time.sleep(0.5)
        # debug(bot)
        bot.run()
        sys.stdout.write('.')
        sys.stdout.flush()
        # except Exception as e:
        #    logging.getLogger('start.loop').error(str(e))


def debug(bot: BombCryptoBot):
    bot._bomb_crypto_image_processor.debug()


if __name__ == '__main__':
    run()
