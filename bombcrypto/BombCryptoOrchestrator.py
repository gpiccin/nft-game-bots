import logging
import time
from typing import List, Optional

from bombcrypto.BombCryptoBot import BombCryptoBot
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider
from modules.Rectangle import Rectangle


class BombCryptoOrchestrator:
    def __init__(self, image_provider: ImageProvider,
                 target_images_loader: ImageLoader):
        self._logger = logging.getLogger(type(self).__name__)
        self._image_provider = image_provider
        self.target_images_loader = target_images_loader
        self._bots = {}
        self._seconds_to_check_bots = 3 * 60
        self._seconds_between_bot_execution = 2.5

    def _remove_bots_not_found(self, read_keys):
        keys_to_remove = []

        for key in self._bots.keys():
            if key not in read_keys:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self._bots.pop(key)

    @staticmethod
    def read_keys(left_corners_rectangles: List[Rectangle]) -> List[str]:
        keys = []

        for left_corner in left_corners_rectangles:
            keys.append(BombCryptoBot.create_id(left_corner))

        return keys

    def read_left_corners(self) -> Optional[List[Rectangle]]:
        image = self._image_provider.screenshot()
        bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider, self.target_images_loader)
        left_corners = bomb_crypto_image_processor.top_left_corner(image)

        if left_corners is None:
            return None

        return left_corners.rectangles()

    def read_bots(self):
        left_corners = self.read_left_corners()

        if left_corners is None:
            return

        keys = BombCryptoOrchestrator.read_keys(left_corners)
        self._remove_bots_not_found(keys)

        for left_corner in left_corners:
            bot_id = BombCryptoBot.create_id(left_corner)

            if bot_id not in self._bots.keys():
                bot_bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider,
                                                                           self.target_images_loader)
                self._bots[bot_id] = BombCryptoBot(left_corner, bot_bomb_crypto_image_processor)

    def has_more_than_one_bot(self):
        return len(self._bots) > 1

    def run(self):
        self.read_bots()

        for bot_key in self._bots:
            bot = self._bots[bot_key]
            self._logger.info('Run bot ' + bot.id)

            if self.has_more_than_one_bot():
                bot.maximize_window()

            while True:
                if not bot.run():
                    break
                else:
                    self._logger.info('Waiting ' + str(self._seconds_between_bot_execution) +
                                      ' seconds to execute a new bot ' + bot.id + ' command')

                    time.sleep(self._seconds_between_bot_execution)

            if self.has_more_than_one_bot():
                bot.return_window_size()

        self._logger.info('Waiting ' + str(self._seconds_to_check_bots) + ' seconds to check bots again')
        time.sleep(self._seconds_to_check_bots)
