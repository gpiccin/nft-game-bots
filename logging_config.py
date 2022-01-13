import os
import logging.config
import time
import yaml


def setup(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    logging.Formatter.converter = time.gmtime
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../', default_path))
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
