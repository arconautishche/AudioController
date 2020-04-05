import argparse
import yaml
import logging

_config = None


def load():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', dest='config_file', default='config.yaml')
    args = parser.parse_args()
    with open(args.config_file) as file:
        global _config
        _config = yaml.safe_load(file.read())
    if "log_level" in config():
        logging.basicConfig()
        logging.getLogger().setLevel(config()["log_level"])


def config():
    return _config
