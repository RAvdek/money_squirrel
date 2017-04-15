import os
import json
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s')


def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

LOGGER = get_logger(__name__)


def load_config(name):

    path = os.path.join(os.getcwd(), 'config', name + '.json')
    LOGGER.info("Loading JSON from %s", path)
    with open(path, "r") as f:
        return json.load(f)
