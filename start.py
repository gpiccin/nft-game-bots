import logging
import sys
import time

from bombcrypto.BombCryptoBot import BombCryptoBot
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.BombCryptoOrchestrator import BombCryptoOrchestrator
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

    bot_orchestrator = BombCryptoOrchestrator(bomb_crypto_image_processor)
    loop(bot_orchestrator)


def loop(bot_orchestrator: BombCryptoOrchestrator):
    while True:
        # try:
        bot_orchestrator.run()
        # except Exception as e:
        #    logging.getLogger('start.loop').error(str(e))


if __name__ == '__main__':
    run()
