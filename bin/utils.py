import os
import json
import logging
import psycopg2
import pandas as pd

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s')


def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.info("Instantiated logger w/ name=%s", name)
    return logger

LOGGER = get_logger(__name__)


def load_config(name):

    path = os.path.join(os.getcwd(), 'config', name + '.json')
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
