import logging
import sys


class Formatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    msg = "%(message)s"

    FORMATS = {
        logging.DEBUG: grey + msg + reset,
        logging.INFO: grey + msg + reset,
        logging.WARNING: yellow + msg + reset,
        logging.ERROR: red + msg + reset,
        logging.CRITICAL: bold_red + msg + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(Formatter())
# Add handler to stdout. Strangely just using basicConfig doesn't work
# May want to change the level to something else
# using an .ini config, or to put FileHandlers.
logger.addHandler(handler)
