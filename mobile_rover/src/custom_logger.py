import logging
import sys


def get_logger(name, level="info"):
    logger = logging.getLogger(name)
    if level == "debug":
        logger.setLevel(logging.DEBUG)
    elif level == "info":
        logger.setLevel(logging.INFO)
    elif level == "warning":
        logger.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt="%(levelname)s: %(filename)s:%(lineno)d | %(message)s")
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
