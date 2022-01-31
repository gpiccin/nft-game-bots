import logging

from bombcrypto.BombCryptoOrchestrator import BombCryptoOrchestrator
from core import logging_config
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider

logging_config.setup()


def is_debug_mode():
    return False


def run():
    # image_provider = ImageProvider('./bombcrypto/test-images', ['heroes-heroes_list-2'])
    image_provider = ImageProvider()
    target_images_loader = ImageLoader('bombcrypto/target-images')

    bot_orchestrator = BombCryptoOrchestrator(image_provider, target_images_loader)
    loop(bot_orchestrator)


def loop(bot_orchestrator: BombCryptoOrchestrator):
    while True:
        try:
            bot_orchestrator.run()
        except Exception as e:
            logging.getLogger('start.loop').error(str(e))


if __name__ == '__main__':
    run()
