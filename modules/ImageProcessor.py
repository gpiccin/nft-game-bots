import random
from typing import List

import cv2
import numpy as np

from modules.ImageLoader import ImageLoader
from modules.Rectangle import Rectangle


class ImageProcessor:
    @staticmethod
    def match_list(source_image, image_loader: ImageLoader, images, threshold, use_gray_scale=True):
        for image_name in images:
            rectangles, image_found = ImageProcessor.match(source_image, image_loader.get_image(image_name),
                                                           threshold, use_gray_scale)

            if image_found:
                return rectangles, image_found

        return [], False

    @staticmethod
    def closest_color(list_of_colors, color):
        colors = np.array(list_of_colors)
        color = np.array(color)
        distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        smallest_distance = colors[index_of_smallest]
        return smallest_distance

    @staticmethod
    def dominant_color(image):
        data = np.reshape(image, (-1, 3))
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

        b, g, r = centers[0].astype(np.int32)
        return r, g, b

    @staticmethod
    def match(source_image, target_image, threshold, use_gray_scale=True, match_method=cv2.TM_CCOEFF_NORMED):
        if source_image is None:
            return None, False

        if use_gray_scale:
            source_gray_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
            target_gray_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
            match_result = cv2.matchTemplate(source_gray_image, target_gray_image, match_method)
        else:
            match_result = cv2.matchTemplate(source_image, target_image, match_method)

        y_loc, x_loc = np.where(match_result >= threshold)

        width = target_image.shape[1]
        height = target_image.shape[0]

        rectangles = []

        for (x, y) in zip(x_loc, y_loc):
            rectangles.append([int(x), int(y), int(width), int(height)])
            rectangles.append([int(x), int(y), int(width), int(height)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        return Rectangle.create_list(rectangles), ImageProcessor._has_target_image(rectangles)

    @staticmethod
    def _has_target_image(rectangles):
        return len(rectangles) > 0

    @staticmethod
    def cut_rectangles(image, rectangle1: Rectangle, rectangle2: Rectangle):
        cut_image = image[rectangle1.top:rectangle2.bottom, rectangle1.left:rectangle2.right]
        return cut_image

    @staticmethod
    def cut_rectangle(image, rectangle: Rectangle):
        cut_image = image[rectangle.top:rectangle.bottom, rectangle.left:rectangle.right]

        return cut_image

    @staticmethod
    def draw_rectangles(image, rectangles: List[Rectangle]):
        for rect in rectangles:
            ImageProcessor.draw_rectangle(image, rect)

    @staticmethod
    def draw_rectangle(image, rectangle: Rectangle):
        cv2.rectangle(image, rectangle.topleft, rectangle.bottomright, ImageProcessor.random_color(), 2)

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
        cv2.circle(image, center_coordinates, 1, ImageProcessor.random_color(), 2)
