import mss
import numpy as np
from src.modules.ImageLoader import ImageLoader


class ImageProvider:
    def __init__(self, images_path=None, image=None):
        if images_path:
            self._images = ImageLoader(images_path)
            self._images.load()

        self._image = image

    def image(self):
        if self._image is not None and self._images is not None:
            return self._images.get_image(self._image)

        return ImageProvider.print_screen(0)

    @staticmethod
    def print_screen(monitor_id: int):
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_id]
            sct_image = np.array(sct.grab(monitor))
            # The screen part to capture
            # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}
            # Grab the data
            return sct_image[:, :, :3]
