from typing import Optional

from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageLoader import ImageLoader
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoBehaviours import ConnectWallet, OkError, Ok, SignOnMetamask, Close, Back, \
    SendAllHeroesToWork, \
    SendHeroToWork, RestHero, TreasureHunt, GoToHeroes, RestAllHeroes, SlideDownToGoHeroes, SlideUpToGoHeroes, RedBar, \
    FullBar, HeroLocalizationBar, GreenBar
from src.modules.Behaviours import Behaviour, Click, Information


class BombCryptoImageProcessor:
    def __init__(self, image_provider: ImageProvider, match_image_threshold=0.8, debug=True):
        self._debug = debug
        self._target_images = None
        self._match_image_threshold = match_image_threshold
        self._image_processor = ImageProcessor()
        self._image_provider = image_provider

    def actions(self) -> []:
        self._target_images = ImageLoader('./bombcrypto/target-images')
        self._target_images.load()

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
            self._append_action(self.rest_all_heroes(image), image_behaviours)
            self._append_action(self.red_bar(image), image_behaviours)
            self._append_action(self.green_bar(image), image_behaviours)
            self._append_action(self.full_bar(image), image_behaviours)
            self._append_action(self.hero_localization_bar(image), image_behaviours)

            self._debug_image(image, image_behaviours)

            behaviours.append(image_behaviours)

        return behaviours

    def connect_wallet(self, image) -> Optional[ConnectWallet]:
        images = ['connect-wallet-button-0', 'connect-wallet-button-1', 'connect-wallet-button-2',
                  'connect-wallet-button-3']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return ConnectWallet(rectangle)

        return None

    def error(self, image) -> Optional[OkError]:
        images = ['error-0', 'error-1001-0', 'error-server-unstable-0']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            generic_ok = self.generic_ok(image)

            if generic_ok:
                return OkError(generic_ok.rectangles())

        return None

    def generic_ok(self, image) -> Optional[Ok]:
        images = ['ok-0', 'ok-1', 'ok-2']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return Ok(rectangle)

        return None

    def sign_metamask(self, image) -> Optional[SignOnMetamask]:
        images = ['sign-metamask-0', 'sign-metamask-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return SignOnMetamask(rectangle)

        return None

    def close(self, image) -> Optional[Close]:
        images = ['close-button-0', 'close-button-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return Close(rectangle)

        return None

    def back(self, image) -> Optional[Back]:
        images = ['back-button-0', 'back-button-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return Back(rectangle)

        return None

    def all_heroes_to_work(self, image) -> Optional[SendAllHeroesToWork]:
        images = ['send-all-heroes-to-work-button-0', 'send-all-heroes-to-work-button-0']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return SendAllHeroesToWork(rectangle)

        return None

    def work(self, image) -> Optional[SendHeroToWork]:
        images = ['work-button-0', 'work-button-1', 'work-button-2']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return SendHeroToWork(rectangle)

        return None

    def rest(self, image) -> Optional[RestHero]:
        images = ['rest-button-0', 'rest-button-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return RestHero(rectangle)

        return None

    def treasure_hunt(self, image) -> Optional[TreasureHunt]:
        images = ['treasure-hunt-0', 'treasure-hunt-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return TreasureHunt(rectangle)

        return None

    def go_to_heroes(self, image) -> Optional[GoToHeroes]:
        images = ['go-to-heroes-0', 'go-to-heroes-1', 'go-to-heroes-2', 'go-to-heroes-3']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return GoToHeroes(rectangle)

        return None

    def slide_up_to_go_heroes(self, image) -> Optional[SlideUpToGoHeroes]:
        images = ['slide-up-go-heroes-0', 'slide-up-go-heroes-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return SlideUpToGoHeroes(rectangle)

        return None

    def slide_down_to_return_to_work(self, image) -> Optional[SlideDownToGoHeroes]:
        images = ['slide-down-go-heroes-0', 'slide-down-go-heroes-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return SlideDownToGoHeroes(rectangle)

        return None

    def rest_all_heroes(self, image) -> Optional[RestAllHeroes]:
        images = ['rest-all-heroes-button-0', 'rest-all-heroes-button-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold)

        if has_image:
            return RestAllHeroes(rectangle)

        return None

    def red_bar(self, image) -> Optional[RedBar]:
        images = ['red-bar-0', 'red-bar-1', 'red-bar-2']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold, False)

        if has_image:
            return RedBar(rectangle)

        return None

    def green_bar(self, image) -> Optional[GreenBar]:
        images = ['green-bar-0', 'green-bar-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold, False)

        if has_image:
            return GreenBar(rectangle)

        return None

    def hero_localization_bar(self, image) -> Optional[HeroLocalizationBar]:
        images = ['hero-bar-0', 'hero-bar-0']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold, True)

        if has_image:
            return HeroLocalizationBar(rectangle)

        return None

    def full_bar(self, image) -> Optional[FullBar]:
        images = ['full-bar-0', 'full-bar-1']
        rectangle, has_image = self._image_processor.match_list(image, self._target_images, images,
                                                                self._match_image_threshold, False)

        if has_image:
            return FullBar(rectangle)

        return None

    def _debug_image(self, image, actions):
        if not self._debug:
            return

        for action in actions:
            if isinstance(action, Click):
                for _ in range(1000):
                    points = action.points()

                    for point in points:
                        ImageProcessor.draw_circle(image, point)

                continue

            if isinstance(action, Information):
                ImageProcessor.draw_rectangles(image, action.rectangles())

        ImageProcessor.show(image)

    @staticmethod
    def _append_action(action, actions):
        if action:
            actions.append(action)
