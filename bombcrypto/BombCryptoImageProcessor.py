from typing import Optional

from modules.ImageProcessor import ImageProcessor
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider
from bombcrypto.BombCryptoBehaviours import ConnectWalletClick, OkErrorClick, OkClick, SignOnMetamaskClick, \
    CloseClick, BackClick, \
    SendAllHeroesToWorkClick, \
    SendHeroToWorkClick, RestHeroClick, TreasureHuntClick, SendHeroesToWorkClick, RestAllHeroesClick, \
    SlideDownToGoHeroesClick, SlideUpToGoHeroesClick, \
    FullBarInformation, HeroLocalizationBar, BeginEnergyBarInformation, EndEnergyBarInformation
from modules.Behaviours import Click, Information


class BombCryptoImageProcessor:
    def __init__(self, image_provider: ImageProvider,
                 target_images_loader: ImageLoader,
                 match_image_threshold=0.8):
        self._target_images = None
        self._match_image_threshold = match_image_threshold
        self._image_provider = image_provider
        self._target_images = target_images_loader
        self._target_images.load()

    def image(self):
        print_screen_image = self._image_provider.image()

        top_left = self.top_left_corner(print_screen_image)

        if top_left is None:
            return None

        # top_right = self.top_right_corner(print_screen_image)
        # bottom_left = self.bottom_left_corner(print_screen_image)
        #
        # trx, tr_y, trw, trh = top_right.first_rectangle()
        # tlx, tly, tlw, tlh = top_left.first_rectangle()
        # blx, bly, blw, blh = bottom_left.first_rectangle()
        #
        # rest_button_image = print_screen_image[tly:bly + blh, tlx:tlx + trx + tlw]

        #ImageProcessor.draw_rectangles(print_screen_image, top_left.rectangles())
        #ImageProcessor.show(print_screen_image)

        return print_screen_image

    def connect_wallet(self, image) -> Optional[ConnectWalletClick]:
        images = ['connect-wallet-button-0', 'connect-wallet-button-1', 'connect-wallet-button-2',
                  'connect-wallet-button-3']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return ConnectWalletClick(rectangle)

        return None

    def error(self, image) -> Optional[OkErrorClick]:
        images = ['error-0', 'error-1001-0', 'error-server-unstable-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            generic_ok = self.generic_ok(image)

            if generic_ok:
                return OkErrorClick(generic_ok.rectangles())

        return None

    def top_left_corner(self, image) -> Optional[Information]:
        images = ['top-left-corner-0', 'top-left-corner-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return Information(rectangle)

        return None

    def top_right_corner(self, image) -> Optional[Information]:
        images = ['top-right-corner-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return Information(rectangle)

        return None

    def bottom_left_corner(self, image) -> Optional[Information]:
        images = ['bottom-left-corner-0', 'bottom-left-corner-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return Information(rectangle)

        return None

    def generic_ok(self, image) -> Optional[OkClick]:
        images = ['ok-0', 'ok-1', 'ok-2']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return OkClick(rectangle)

        return None

    def sign_metamask(self, image) -> Optional[SignOnMetamaskClick]:
        images = ['sign-metamask-0', 'sign-metamask-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return SignOnMetamaskClick(rectangle)

        return None

    def close(self, image) -> Optional[CloseClick]:
        images = ['close-button-0', 'close-button-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return CloseClick(rectangle)

        return None

    def back(self, image) -> Optional[BackClick]:
        images = ['back-button-0', 'back-button-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return BackClick(rectangle)

        return None

    def all_heroes_to_work(self, image) -> Optional[SendAllHeroesToWorkClick]:
        images = ['send-all-heroes-to-work-button-0', 'send-all-heroes-to-work-button-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold, use_gray_scale=False)

        if has_image:
            return SendAllHeroesToWorkClick(rectangle)

        return None

    def work(self, image) -> Optional[SendHeroToWorkClick]:
        images = ['work-button-0', 'work-button-1', 'work-button-2']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return SendHeroToWorkClick(rectangle)

        return None

    def rest(self, image) -> Optional[RestHeroClick]:
        images = ['rest-button-0', 'rest-button-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return RestHeroClick(rectangle)

        return None

    def treasure_hunt(self, image) -> Optional[TreasureHuntClick]:
        images = ['treasure-hunt-0', 'treasure-hunt-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return TreasureHuntClick(rectangle)

        return None

    def go_to_heroes(self, image) -> Optional[SendHeroesToWorkClick]:
        images = ['go-to-heroes-0', 'go-to-heroes-1', 'go-to-heroes-2']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return SendHeroesToWorkClick(rectangle)

        return None

    def slide_up_to_go_heroes(self, image) -> Optional[SlideUpToGoHeroesClick]:
        images = ['slide-up-go-heroes-0', 'slide-up-go-heroes-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return SlideUpToGoHeroesClick(rectangle)

        return None

    def slide_down_to_return_to_work(self, image) -> Optional[SlideDownToGoHeroesClick]:
        images = ['slide-down-go-heroes-0', 'slide-down-go-heroes-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return SlideDownToGoHeroesClick(rectangle)

        return None

    def all_heroes_to_rest(self, image) -> Optional[RestAllHeroesClick]:
        images = ['rest-all-heroes-button-0', 'rest-all-heroes-button-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return RestAllHeroesClick(rectangle)

        return None

    def begin_energy_bar(self, image) -> Optional[BeginEnergyBarInformation]:
        images = ['begin-bar-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return BeginEnergyBarInformation(rectangle)

        return None

    def end_energy_bar(self, image) -> Optional[EndEnergyBarInformation]:
        images = ['end-bar-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return EndEnergyBarInformation(rectangle)

        return None

    def hero_bar(self, image) -> Optional[HeroLocalizationBar]:
        images = ['hero-bar-0', 'hero-bar-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return HeroLocalizationBar(rectangle)

        return None

    def character_title(self, image) -> Optional[Information]:
        images = ['character-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return Information(rectangle)

        return None

    def full_bar(self, image) -> Optional[FullBarInformation]:
        images = ['full-label-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return FullBarInformation(rectangle)

        return None

    def bombcrypto_logo(self, image) -> Optional[Information]:
        images = ['bomb-logo-0', 'bomb-logo-0']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return Information(rectangle)

        return None

    def coin(self, image) -> Optional[Click]:
        images = ['coin-0', 'coin-1']
        rectangle, has_image = ImageProcessor.match_list(image, self._target_images, images,
                                                         self._match_image_threshold)

        if has_image:
            return Click(rectangle)

        return None

    def is_in_the_heroes_screen(self, image):
        return self.hero_bar(image) is not None

    def is_all_working(self, image):
        return self.all_heroes_to_work(image) is None

    def is_in_the_game_play_screen(self, image):
        return self.back(image) is not None

    def is_sign_screen(self, image):
        return self.sign_metamask(image) is not None

    def is_playing(self, image):
        return self.slide_up_to_go_heroes(image) is not None

    def is_loading_screen(self, image):
        return self.bombcrypto_logo(image) is not None and self.connect_wallet(image) is None

    def is_treasure_hunt_screen(self, image):
        return self.treasure_hunt(image) is not None

    def is_signed(self, image):
        return not self.is_connect_wallet_screen(image) or self.is_treasure_hunt_screen(image)

    def is_connect_wallet_screen(self, image):
        return self.connect_wallet(image) is not None

    def debug(self):
        images = self._image_provider.images()

        behaviours = []

        for image in images:
            image_behaviours = []

            self._append_action(self.connect_wallet(image), image_behaviours)
            self._append_action(self.error(image), image_behaviours)
            self._append_action(self.generic_ok(image), image_behaviours)
            self._append_action(self.sign_metamask(image), image_behaviours)
            self._append_action(self.close(image), image_behaviours)
            self._append_action(self.back(image), image_behaviours)
            self._append_action(self.all_heroes_to_work(image), image_behaviours)
            self._append_action(self.work(image), image_behaviours)
            self._append_action(self.rest(image), image_behaviours)
            self._append_action(self.treasure_hunt(image), image_behaviours)
            self._append_action(self.go_to_heroes(image), image_behaviours)
            self._append_action(self.slide_down_to_return_to_work(image), image_behaviours)
            self._append_action(self.slide_up_to_go_heroes(image), image_behaviours)
            self._append_action(self.all_heroes_to_rest(image), image_behaviours)
            self._append_action(self.full_bar(image), image_behaviours)
            self._append_action(self.hero_bar(image), image_behaviours)
            self._append_action(self.bombcrypto_logo(image), image_behaviours)
            self._append_action(self.character_title(image), image_behaviours)
            self._append_action(self.coin(image), image_behaviours)

            self.debug_image(image, image_behaviours)

            behaviours.append(image_behaviours)

        return behaviours

    @staticmethod
    def debug_image(image, actions):
        debug_image = image.copy()

        for action in actions:
            if isinstance(action, Click):
                for _ in range(1000):
                    points = action.random_points()

                    for point in points:
                        ImageProcessor.draw_circle(debug_image, point)

                continue

            if isinstance(action, Information):
                ImageProcessor.draw_rectangles(debug_image, action.rectangles())

        ImageProcessor.show(debug_image)

    @staticmethod
    def _append_action(action, actions):
        if action:
            actions.append(action)
