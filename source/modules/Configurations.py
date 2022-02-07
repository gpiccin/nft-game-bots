import yaml


class Configurations:
    def __init__(self):
        self._image_analysis_config = None

    def load(self):
        stream = open("config.yaml", 'r')
        config = yaml.safe_load(stream)
        self._image_analysis_config = config['image_analysis']

    def image_analysis_accuracy(self) -> float:
        return self._image_analysis_config['accuracy']
