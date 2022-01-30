import hashlib
import logging

import cv2

from bombcrypto.Hero import Hero
from modules.ImageProcessor import ImageProcessor


class HeroList:
    def __init__(self):
        self._heroes = []
        self._logger = logging.getLogger(type(self).__name__)

    def __len__(self):
        return len(self._heroes)

    def __iter__(self):
        return iter(self._heroes)

    def add_list(self, list):
        if not list:
            return

        for hero in list:
            self.add(hero)

    def add(self, hero: Hero):
        searched_hero = self.get_hero(hero.id_image, 1.0)

        if hero and not searched_hero:
            self._heroes.append(hero)
        else:
            self._logger.info('Duplicated hero: ' + hero.id + ' with hero: ' + searched_hero.id)

    def clean(self):
        self._heroes = []

    def heroes(self):
        return self._heroes

    def reversed_heroes(self):
        return list(reversed(self._heroes))

    def get_hero(self, id_image, threshold):
        hero, is_hero = self._contains_hero(id_image, threshold=threshold)

        if is_hero:
            return hero

        return None

    def _contains_hero(self, id_image, threshold):
        for hero in self.reversed_heroes():
            hero_rectangle, is_hero = ImageProcessor.match(hero.id_image,
                                                           id_image, threshold,
                                                           use_gray_scale=False,
                                                           match_method=cv2.TM_CCOEFF_NORMED)

            # hash = hashlib.md5(id_image).hexdigest()
            # is_hero = hero.id == hash

            if is_hero:
                return hero, is_hero

        return None, False

    def contains_hero(self, id_image):
        hero, is_hero = self._contains_hero(id_image)
        return is_hero
