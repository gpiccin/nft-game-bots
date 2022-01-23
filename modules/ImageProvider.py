import logging

import mss
import numpy as np

from modules.ImageLoader import ImageLoader


class ImageProvider:
    def __init__(self, images_path=None, image_names=None):
        self._logger = logging.getLogger(type(self).__name__)
        self._image_loader = None

        if images_path:
            self._image_loader = ImageLoader(images_path)
            self._image_loader.load()

        self._image_names = image_names

    def images(self) -> []:
        if self._image_loader:
            if self._image_names:
                return self.load_images(self._image_names)
            else:
                return self.load_images(self._image_loader.get_file_names())

        return [ImageProvider.print_screen(0)]

    def image(self):
        if self._image_loader:
            if self._image_names:
                return self.load_images([self._image_names[0]])[0]
            else:
                return self.load_images([self._image_loader.get_file_names()[0]])[0]

        self._logger.debug('Print screen')
        return ImageProvider.print_screen(0)

    def load_images(self, image_names):
        images = []

        for image_name in image_names:
            images.append(self._image_loader.get_image(image_name))

        return images

    @staticmethod
    def print_screen(monitor_id: int):
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_id]
            sct_image = np.array(sct.grab(monitor))
            # The screen part to capture
            # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}
            # Grab the data
            return sct_image[:, :, :3]
