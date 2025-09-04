from loguru import logger as log


class Logger:
    logger: log

    def __init__(self):
        self.logger = log

        self.debug = log.debug
        self.info = log.info
        self.warning = log.warning
        self.error = log.error
        self.success = log.success


logger = Logger()