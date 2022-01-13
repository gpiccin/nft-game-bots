from os import listdir
import cv2


class ImageLoader:
    def __init__(self, folder_path):
        self._images = None
        self.folder_path = folder_path

    def load(self):
        file_names = listdir(self.folder_path)
        loaded_images = {}

        for file in file_names:
            path = self.folder_path.replace('./', '') + '/' + file
            loaded_images[file[:file.find('.')]] = cv2.imread(path)

        self._images = loaded_images

    def get_image(self, name):
        return self._images[name]