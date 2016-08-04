from __future__ import unicode_literals
import time

import logging
logger = logging.getLogger(__file__)

try:
    import lcd
    lcd = lcd.lcd()
    # Change this to your i2c address
    lcd.set_addr(0x23)
except Exception:
    lcd = False


class LcdHandler(logging.Handler):
    fmt = '%(asctime)s %(message)s'
    datefmt = '%H:%M:%S'

    def __init__(self):
        logging.Handler.__init__(self)
        self.formatter = logging.Formatter(fmt, datefmt)

    def emit(self, record):
        if record:
            lcd.message(self.formatter.format(record))

class LogFormatter(logging.Formatter):
    RESET_SEQ = '\033[0m'
    COLOR_SEQ = '\033[1;%s'

    color_hex = {
        'ERROR': '91m',
        'red': '91m',
        'DEBUG': '92m',
        'green': '92m',
        'WARNING': '93m',
        'yellow': '93m',
        'blue': '94m',
        'INFO': '96m',
        'cyan': '96m',
        'VERBOSE': '37m',
        'white': '37m'
    }

    fmt = '%(asctime)s %(message)s'
    datefmt = '%H:%M:%S'

    def __init__(self, fmt=fmt, datefmt=datefmt):
        super(LogFormatter, self).__init__(fmt, datefmt)

    def get_color(self, record):
        # We default to white
        return self.color_hex.get(record.levelname, LogFormatter.color_hex['white'])

    def format(self, record):
        level = record.levelname
        color = self.get_color(record)
        record.msg = '{color}{message}{reset}'.format(color=LogFormatter.COLOR_SEQ % (color), message=record.msg, reset=LogFormatter.RESET_SEQ)
#        record.msg = '{color}{message}'.format(color='', message=record.msg)
        result = logging.Formatter.format(self, record)
        return result

VERBOSE_LEVELV_NUM = 5
WHITE_LEVELV_NUM = 21
GREEN_LEVELV_NUM = 22
YELLOW_LEVELV_NUM = 23
BLUE_LEVELV_NUM = 24
CYAN_LEVELV_NUM = 25
RED_LEVELV_NUM = 26
def custom_logging_level_handler(self, level, message, args, kwargs):
    if self.isEnabledFor(level):
        self._log(level, message, args, **kwargs)
def verbose(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, VERBOSE_LEVELV_NUM, message, args, kwargs)
def white(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, WHITE_LEVELV_NUM, message, args, kwargs)
def green(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, GREEN_LEVELV_NUM, message, args, kwargs)
def yellow(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, YELLOW_LEVELV_NUM, message, args, kwargs)
def blue(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, BLUE_LEVELV_NUM, message, args, kwargs)
def cyan(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, CYAN_LEVELV_NUM, message, args, kwargs)
def red(self, message, *args, **kwargs):
    return custom_logging_level_handler(self, RED_LEVELV_NUM, message, args, kwargs)

logging.Logger.verbose = verbose
logging.addLevelName(VERBOSE_LEVELV_NUM, 'verbose')
logging.Logger.white = white
logging.addLevelName(WHITE_LEVELV_NUM, 'white')
logging.Logger.green = green
logging.addLevelName(GREEN_LEVELV_NUM, 'green')
logging.Logger.yellow = yellow
logging.addLevelName(YELLOW_LEVELV_NUM, 'yellow')
logging.Logger.blue = blue
logging.addLevelName(BLUE_LEVELV_NUM, 'blue')
logging.Logger.cyan = cyan
logging.addLevelName(CYAN_LEVELV_NUM, 'cyan')
logging.Logger.red = red
logging.addLevelName(RED_LEVELV_NUM, 'red')


root = logging.getLogger()
if lcd:
    root.addHandler(logger.LcdHandler())

logger = logging.getLogger(__name__)

def error(string):
    logger.error(string)
def warn(string):
    logger.warn(string)
def info(string):
    logger.info(string)
def debug(string):
    logger.debug(string)
def verbose(string):
    logger.verbose(string)

def white(string):
    logger.white(string)
def green(string):
    logger.green(string)
def yellow(string):
    logger.yellow(string)
def blue(string):
    logger.blue(string)
def cyan(string):
    logger.cyan(string)
def red(string):
    logger.red(string)

def log(string, color='white'):
    func = getattr(logger, color, None)
    if func is None:
        func = logger.white
    func(string)

