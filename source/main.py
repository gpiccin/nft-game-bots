import multiprocessing

from source.bombcrypto.BombCryptoOrchestrator import BombCryptoOrchestrator
from source.core import logging_config
from source.modules.ImageLoader import ImageLoader
from source.modules.ImageProvider import ImageProvider
from source.ui.server.WebServer import WebServer

logging_config.setup()


def start_bot_orchestrator():
    # image_provider = ImageProvider('./bombcrypto/test-images', ['heroes-heroes_list-2'])
    image_provider = ImageProvider()
    target_images_loader = ImageLoader('bombcrypto/target-images')

    bot_orchestrator = BombCryptoOrchestrator(image_provider, target_images_loader)
    bot_orchestrator.start()


if __name__ == '__main__':
    web_server = WebServer()

    bot_process = multiprocessing.Process(target=start_bot_orchestrator)
    web_server_process = multiprocessing.Process(target=web_server.start)

    bot_process.start()
    web_server_process.start()
    bot_process.join()
    web_server_process.join()
