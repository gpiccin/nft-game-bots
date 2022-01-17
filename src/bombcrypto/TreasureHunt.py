#38.34
from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.modules.ActionExecutor import ActionExecutor
from src.modules.MethodExecutor import MethodExecutor
from src.modules.TimeControl import TimeControl


class TreasureHunt:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._time_after_click = TimeControl(1)
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        treasure_hunt_click = self._image_processor.treasure_hunt(image)

        if treasure_hunt_click:
            MethodExecutor.execute(self.go_to_treasure_hunt,
                                   [image],
                                   self._image_processor.is_in_the_game_play_screen,
                                   [self._image_processor.image])

    def go_to_treasure_hunt(self, image):
        treasure_hunt = self._image_processor.treasure_hunt(image)

        if treasure_hunt:
            ActionExecutor.click(treasure_hunt.first_point())