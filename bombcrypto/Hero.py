import base64
import hashlib
import logging

import cv2

from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ImageProcessor import ImageProcessor
from modules.Rectangle import Rectangle


class Hero:
    UNKNOWN_ENERGY = 0
    FULL_ENERGY = 3
    GREEN_ENERGY = 2
    RED_ENERGY = 1

    def __init__(self, image,
                 bar_rectangle, rest_rectangle,
                 work_rectangle,
                 image_processor: BombCryptoImageProcessor):

        self._logger = logging.getLogger(type(self).__name__)
        self._image = image
        self._bar_rectangle = bar_rectangle
        self._rest_rectangle = rest_rectangle
        self._work_rectangle = work_rectangle
        self._image_processor = image_processor

        self.id = None
        self.id_image = None
        self.type = type
        self.energy_level = None
        self.is_resting = None
        self._set_hero_information(bar_rectangle,
                                   rest_rectangle)

    def work_rectangle(self):
        return self._work_rectangle

    def _set_hero_information(self, bar_rectangle, rest_rectangle):

        x_bar, y_bar, w_bar, h_bar = bar_rectangle
        x_rest, y_rest, w_rest, h_rest = rest_rectangle

        hero_line_image = self._image[y_bar:y_bar + h_bar,
                          x_bar:x_bar + x_rest - x_bar + w_rest]

        hero_id_image = self._image[y_bar:y_bar + int(h_bar / 2),
                        x_bar + w_bar + 2:x_bar + w_bar + 2 + int(w_bar * 9.8)]

        # ImageProcessor.show(hero_line_image)

        self._set_id(hero_id_image)
        self._set_energy(hero_line_image)
        self._set_state(self._image[y_rest:y_rest + h_rest, x_rest:x_rest + w_rest])

    def _set_state(self, image):
        color_found = ImageProcessor.dominant_color(image)
        color = [color_found[0], color_found[1], color_found[2]]

        list_of_colors = [[169, 124, 79], [221, 158, 93]]
        closest_color = ImageProcessor.closest_color(list_of_colors, color)

        self.is_resting = closest_color[0][0] == 221

    def _set_id(self, id_image):
        gray_id_image = cv2.cvtColor(id_image, cv2.COLOR_BGR2YUV)
        # (thresh, black_and_white_id_image) = cv2.threshold(gray_id_image, 150, 255, cv2.THRESH_BINARY)
        #
        black_and_white_id_image_base64 = base64.b64encode(gray_id_image)
        #ImageProcessor.show(id_image, 'Finding')

        self.id = hashlib.md5(gray_id_image).hexdigest()
        self.id_image = gray_id_image

    def _set_energy(self, hero_line_image):
        energy_bar = self._image_processor.full_bar(hero_line_image)

        if energy_bar:
            self.energy_level = Hero.FULL_ENERGY
            return

        energy_bar_image = self._get_energy_bar_image(hero_line_image)

        if BombCryptoImageProcessor.is_hero_energy_bar_green(energy_bar_image):
            self.energy_level = Hero.GREEN_ENERGY
            return

        self.energy_level = Hero.RED_ENERGY

    def _get_energy_bar_image(self, hero_line_image):
        begin_energy_bar = self._image_processor.begin_energy_bar(hero_line_image)
        end_energy_bar = self._image_processor.end_energy_bar(hero_line_image)

        begin_energy_bar_rect = Rectangle( begin_energy_bar.first_rectangle())

        x_begin_energy_bar, y_begin_energy_bar, \
        w_begin_energy_bar, h_begin_energy_bar = \
            begin_energy_bar.first_rectangle()

        x_end_energy_bar, y_end_energy_bar, \
        w_end_energy_bar, h_end_energy_bar = \
            end_energy_bar.first_rectangle()

        image = hero_line_image[y_begin_energy_bar:y_begin_energy_bar + h_end_energy_bar,
                x_begin_energy_bar:x_end_energy_bar + w_end_energy_bar]

        return image
