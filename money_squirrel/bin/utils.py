import os
import json
import logging
import psycopg2
import pandas as pd

logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
ISO_DAILY = '%Y-%m-%d'
ISO_HOURLY = '%Y-%m-%dT%H'
ISO = '%Y-%m-%dT%H:%M:%S'


def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.info("Instantiated logger w/ name=%s", name)
    return logger

LOGGER = get_logger(__name__)


def load_config(name):

    app_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(app_path, 'config', name + '.json')
    LOGGER.info("Loading JSON from %s", path)
    with open(path, "r") as f:
        return json.load(f)


def get_pg_connection(env="local"):

    config = load_config("postgres")[env]
    con_str = "host='{host}' dbname='{dbname}' user='{user}'"
    con_str = con_str.format(**config)
    LOGGER.info("Connecting to postgres DB @ %s", config['host'])
    return psycopg2.connect(con_str)


def query_pg(query, env="local"):

    con = get_pg_connection(env)
    LOGGER.info("Executing query:\n\n%s\n", query)
    return pd.read_sql(query, con=con)