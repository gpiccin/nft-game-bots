from os import listdir
import cv2


class ImageLoader:
    def __init__(self, folder_path):
        self._images = None
        self.folder_path = folder_path
        self._file_names = []

    def load(self):
        file_names = listdir(self.folder_path)
        loaded_images = {}

        for file in file_names:
            path = self.folder_path.replace('./', '') + '/' + file
            file_name = file[:file.find('.')]

            image = cv2.imread(path)

            if image is not None:
                self._file_names.append(file_name)
                loaded_images[file_name] = image

        self._images = loaded_images

    def get_file_names(self):
        return self._file_names

    def get_image(self, name):
        return self._images[name]
