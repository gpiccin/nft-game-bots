#38.34
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class TreasureHunt:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        treasure_hunt_click = self._image_processor.treasure_hunt(image)

        if treasure_hunt_click:
            execution_result = MethodExecutor.execute(self.go_to_treasure_hunt,
                                   [image],
                                   self._image_processor.is_in_the_game_play_screen,
                                   [self._image_processor.image])

            if execution_result == MethodExecutor.SUCCESS:
                return True

        return False

    def go_to_treasure_hunt(self, image):
        treasure_hunt = self._image_processor.treasure_hunt(image)

        if treasure_hunt:
            ActionExecutor.click(treasure_hunt.first_point())