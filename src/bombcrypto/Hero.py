import re
import uuid

from pytesseract import pytesseract

from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.modules.ActionExecutor import ActionExecutor


class Hero:
    UNKNOWN_ENERGY = 0
    FULL_ENERGY = 3
    GREEN_ENERGY = 2
    RED_ENERGY = 1

    def __init__(self, hero_id_image, hero_line_image,
                 image_processor: BombCryptoImageProcessor, is_resting):
        self.is_resting = is_resting
        self.id = None
        self.type = type
        self.energy_level = None
        self._image_processor = image_processor
        self._set_id(hero_id_image)
        self._set_energy(hero_line_image)

    def set_type(self, type_image):
        self.type = None

    def _set_id(self, id_image):
        id_text = pytesseract.image_to_string(id_image)
        id = re.findall(r'\d+', id_text)

        if len(id) > 0:
            self.id = id[0]
        else:
            self.id = str(uuid.uuid1())

        self._id_image = id_image

    def send_to_work(self):
        ActionExecutor.click(self._work_button_point)

    def _send_to_work(self):
        ActionExecutor.click(self._work_button_point)

    def rest(self):
        ActionExecutor.click(self._rest_button_point)

    def _rest(self):
        ActionExecutor.click(self._rest_button_point)

    def _set_energy(self, hero_line_image):
        energy_bar = self._image_processor.red_bar(hero_line_image)

        if energy_bar:
            self.energy_level = Hero.RED_ENERGY
            return

        energy_bar = self._image_processor.full_bar(hero_line_image)

        if energy_bar:
            self.energy_level = Hero.FULL_ENERGY
            return

        energy_bar = self._image_processor.green_bar(hero_line_image)

        if energy_bar:
            self.energy_level = Hero.GREEN_ENERGY

        self.energy_level = Hero.UNKNOWN_ENERGY
