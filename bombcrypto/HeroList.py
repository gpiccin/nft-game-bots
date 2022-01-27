import logging

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

    def __reversed__(self):
        return self._heroes

    def add_list(self, list):
        if not list:
            return

        for hero in list:
            self.add(hero)

    def add(self, hero: Hero):
        if hero and not self.contains_hero(hero.id_image):
            self._heroes.append(hero)

    def clean(self):
        self._heroes = []

    def heroes(self):
        return self._heroes

    def reversed_heroes(self):
        return list(reversed(self._heroes))

    def get_hero(self, id_image):
        hero, is_hero = self._contains_hero(id_image)

        if is_hero:
            return hero

        return None

    def _contains_hero(self, id_image):
        # ImageProcessor.show(id_image, 'Finding')

        for hero in self._heroes:
            # ImageProcessor.show(hero.id_image)
            hero_rectangle, is_hero = ImageProcessor.match(hero.id_image,
                                                           id_image, 0.9,
                                                           use_gray_scale=False)

            # self._logger.info(is_hero)
            if is_hero:
                return hero, is_hero

        return None, False

    def contains_hero(self, id_image):
        hero, is_hero = self._contains_hero(id_image)
        return is_hero
