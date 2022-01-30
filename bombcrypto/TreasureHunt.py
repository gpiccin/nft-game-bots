from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class TreasureHunt:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        treasure_hunt_click = self._image_processor.treasure_hunt(image)

        if not treasure_hunt_click:
            return False

        MethodExecutor.execute(self.go_to_treasure_hunt,
                               [image],
                               self._image_processor.is_in_the_game_play_screen,
                               [self._image_processor.game_screenshot])

        return True

    def go_to_treasure_hunt(self, image):
        treasure_hunt = self._image_processor.treasure_hunt(image)

        if treasure_hunt:
            self._action_executor.click(treasure_hunt.single_random_point())
