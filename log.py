import logging


class ColoredFormatter(logging.Formatter):
    def __init__(self, style="[%(levelname)s] - [%(name)s] - %(asctime)s - %(message)s"):
        super().__init__(style)
        self.COLOR_CODES = {
            # logging.DEBUG: "\033[0m",  # White
            logging.INFO: "\033[32m",  # Green
            logging.WARNING: "\033[33m",  # Yellow
            logging.ERROR: "\033[91m",  # Red
            logging.CRITICAL: "\x1b[31;1m",  # Bold Red
        }

    def format(self, record):
        color_code = self.COLOR_CODES.get(record.levelno)
        if color_code:
            record.levelname = f"{color_code}{record.levelname}\033[0m"
        return super().format(record)


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = ColoredFormatter()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
