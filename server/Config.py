import argparse
import yaml
import logging
import time
from pathlib import Path
import os.path

_config = None


def load():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', dest='config_file', default='config.yaml')
    args = parser.parse_args()
    with open(args.config_file) as file:
        global _config
        _config = yaml.safe_load(file.read())
    if 'logging' in config():
        log_config = config()['logging']
        logger = logging.getLogger()
        if "log_level" in log_config:
            logging.basicConfig()
            logger.setLevel(log_config["log_level"])
        if "log_file" in log_config:
            now = time.strftime('%Y-%m-%d_%H.%M')
            filename = log_config['log_file'].format(now=now)
            Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(filename)
            formatter = logging.Formatter("%(asctime)s : %(levelname)-8s %(message)s")
            fh.setFormatter(formatter)
            logger.addHandler(fh)


def config():
    return _config
