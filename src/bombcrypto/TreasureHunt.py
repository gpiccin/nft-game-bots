#38.34
from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.modules.ActionExecutor import ActionExecutor
from src.modules.TimeControl import TimeControl


class TreasureHunt:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._time_after_click = TimeControl(1)
        self._bomb_crypto_image_processor = bomb_crypto_image_processor

    def run(self, image):
        treasure_hunt_click = self._bomb_crypto_image_processor.treasure_hunt(image)

        if treasure_hunt_click and self._time_after_click.is_expired():
            ActionExecutor.click(treasure_hunt_click.first_point())
            self._time_after_click.start()