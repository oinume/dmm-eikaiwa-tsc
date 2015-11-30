import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger()


def initialize(level: str=None):
    global logger
    if level:
        level = logging.getLevelName(level.upper())
    else:
        level = logging.DEBUG
    kwargs = {"level": level, "format": "[%(levelname)s] %(message)s"}
    logging.basicConfig(**kwargs)
    logger = logging.getLogger("tsc")
    return logger
