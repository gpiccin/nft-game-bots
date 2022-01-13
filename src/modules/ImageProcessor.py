import cv2
import numpy as np
import mss
import random

from src.modules.ImageLoader import ImageLoader


class ImageProcessor:
    def __init__(self, debug):
        self.debug = debug

    def match_list(self, source_image,  image_loader: ImageLoader, images, threshold):
        for image_name in images:
            rectangles, image_found = self._image_processor.match(source_image,
                                                                  image_loader.get_image(image_name),
                                                                  threshold)

            if image_found:
                return rectangles, image_found

        return [], False

    def match(self, source_image, target_image, threshold):
        """Search for image in the source image
          Parameters:
              source_image: The image that contains the image.
              target_image: The image that will be used as a template to find where to click.
              threshold(float): How confident the bot needs to be to click the buttons (values from 0 to 1)
          """
        match_result = cv2.matchTemplate(source_image, target_image, cv2.TM_CCOEFF_NORMED)

        width = target_image.shape[1]
        height = target_image.shape[0]

        yloc, xloc = np.where(match_result >= threshold)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(width), int(height)])
            rectangles.append([int(x), int(y), int(width), int(height)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        if self.debug:
            self._show_rectangle(source_image, rectangles)

        return rectangles, self._has_target_image(rectangles)

    @staticmethod
    def print_screen(monitor_id: int):
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_id]
            sct_image = np.array(sct.grab(monitor))
            # The screen part to capture
            # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

            # Grab the data
            return sct_image[:, :, :3]

    @staticmethod
    def _has_target_image(rectangles):
        return len(rectangles) != 0

    @staticmethod
    def _show_rectangle(source_image, rectangles):
        """ Show a popup with rectangles showing the rectangles[(x, y, w, h),...]"""

        for (x, y, w, h) in rectangles:
            cv2.rectangle(source_image, (x, y), (x + w, y + h), (255, 255, 255, 255), 2)

        cv2.imshow('Rectangles found', source_image)
        cv2.waitKey(0)
