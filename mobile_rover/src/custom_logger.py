import logging
import sys


def get_logger(name, level="info"):
    logger = logging.getLogger(name)
    if level == "debug":
        logger.setLevel(logging.DEBUG)
    elif level == "info":
        logger.setLevel(logging.INFO)
    elif level == "warning" or level == "warn":
        logger.setLevel(logging.WARNING)

    # INFO: mission.py:21 | Loaded 3 waypoints from mission.csv
    formatter = logging.Formatter(fmt="{levelname:>7s}: {filename}:{lineno:<4} | {message}", style="{")
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
