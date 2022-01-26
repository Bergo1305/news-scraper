import logging


def get_logger(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    stdout_logger = logging.StreamHandler()
    stdout_logger.setFormatter(
        logging.Formatter(
            '[%(name)s:%(filename)s:%(lineno)d] - [%(process)d] - %(asctime)s - %(levelname)s - %(message)s'
        )
    )

    logger.addHandler(stdout_logger)
    logger.propagate = False

    return logger


LOGGER = get_logger("NEWS-SCRAPER-LOGGER")