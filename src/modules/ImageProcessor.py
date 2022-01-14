import random

import cv2
import numpy as np
from src.modules.ImageLoader import ImageLoader


class ImageProcessor:
    def match_list(self, source_image,  image_loader: ImageLoader, images, threshold):
        for image_name in images:
            rectangles, image_found = self.match(source_image, image_loader.get_image(image_name), threshold)

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

        source_gray_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        target_gray_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

        match_result = cv2.matchTemplate(source_gray_image, target_gray_image, cv2.TM_CCOEFF_NORMED)

        width = target_image.shape[1]
        height = target_image.shape[0]

        yloc, xloc = np.where(match_result >= threshold)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(width), int(height)])
            rectangles.append([int(x), int(y), int(width), int(height)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        return rectangles, self._has_target_image(rectangles)

    @staticmethod
    def _has_target_image(rectangles):
        return len(rectangles) != 0

    @staticmethod
    def draw_rectangles(image, rectangles):
        for (x, y, w, h) in rectangles:
            cv2.rectangle(image, (x, y), (x + w, y + h), ImageProcessor.random_color(), 2)

    @staticmethod
    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    @staticmethod
    def show_circle(image, center_coordinates):
        cv2.circle(image, center_coordinates, 2, ImageProcessor.random_color(), 2)
        ImageProcessor.show(image)

    @staticmethod
    def show(image, title='Sample'):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_circle(image, center_coordinates):
        cv2.circle(image, center_coordinates, 1, ImageProcessor.random_color(), 1)
