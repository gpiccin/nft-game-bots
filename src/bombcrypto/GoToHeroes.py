from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.modules.MethodExecutor import MethodExecutor
from src.modules.ActionExecutor import ActionExecutor
from src.modules.TimeControl import TimeControl


class GoToHeroes:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._time_to_check_heroes = TimeControl(60 * 3)
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._time_to_check_heroes.is_expired():
            return

        if self._image_processor.is_in_the_heroes_screen(image):
            return

        if not self._image_processor.is_in_the_game_play_screen(image):
            return

        is_go_heroes_button_visible = self.go_to_heroes_from_game_play(image)

        if is_go_heroes_button_visible:
            executed = MethodExecutor.execute(self.go_to_heroes_list,
                                              [self._image_processor.image],
                                              self._image_processor.is_in_the_heroes_screen,
                                              [self._image_processor.image])

            if executed:
                self._time_to_check_heroes.start()

    def go_to_heroes_list(self, image):
        go_to_heroes = self._image_processor.go_to_heroes(image)

        if go_to_heroes:
            ActionExecutor.click(go_to_heroes.first_point())
            return True

        return False

    def go_to_heroes_from_game_play(self, image):
        if not self._image_processor.is_in_the_game_play_screen(image):
            return False

        return MethodExecutor.execute(self.slide_to_get_access_go_heroes_button,
                                      [image],
                                      self._image_processor.go_to_heroes,
                                      [self._image_processor.image])

    def slide_to_get_access_go_heroes_button(self, image):
        slide_up_to_go_heroes = self._image_processor.slide_up_to_go_heroes(image)

        if slide_up_to_go_heroes:
            ActionExecutor.click(slide_up_to_go_heroes.first_point())
            return True

        return False
