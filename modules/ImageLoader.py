import os
import sys
import cv2
import pathlib


class ImageLoader:
    def __init__(self, folder_path):
        self._images = None
        self.folder_path = os.path.normpath(folder_path)
        self._file_names = []

    def load(self):
        application_path = None

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = pathlib.Path().resolve()

        file_names = os.listdir(os.path.join(application_path, self.folder_path))
        loaded_images = {}

        for file in file_names:
            path = os.path.join(application_path, self.folder_path, file)
            file_name = file[:file.find(b'.')]

            image = cv2.imread(path)

            if image is not None:
                self._file_names.append(file_name)
                loaded_images[file_name] = image

        self._images = loaded_images

    def get_file_names(self):
        return self._file_names

    def get_image(self, name):
        return self._images[name]
