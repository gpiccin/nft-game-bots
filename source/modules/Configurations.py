import logging

import yaml


class Configurations:
    def __init__(self):
        self._image_analysis_config = None
        self._logger = logging.getLogger(type(self).__name__)

    def load(self):
        stream = open("config.yaml", 'r')
        config = yaml.safe_load(stream)
        self._image_analysis_config = config['image_analysis']

        for key in self._image_analysis_config:
            self._logger.info('image_analysis.' + key + ': ' + str(self._image_analysis_config[key]))

    def image_analysis_accuracy(self) -> float:
        return self._image_analysis_config['accuracy']
