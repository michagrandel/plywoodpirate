# <> with ❤️ by Micha Grandel - hello@michagrandel.eu
""" Provide functionality for logging in different scenarios """

import logging
import sys

from plywoodpirate.string import color as clicolor, strip_ansi

_format = '%(asctime)s {"level"="%(levelname)s"} %(message)s'
_format = '%(levelname)s: %(message)s'
_datefmt = "%Y-%m-%dT%H:%M:%S"

_handler = logging.StreamHandler(stream=sys.stdout)
_handler.setFormatter(logging.Formatter(_format, datefmt=_datefmt))

#logging.basicConfig(level=logging.INFO, handlers=[_handler])


class Logger(logging.Logger):
    """ Replacment for logging.Logger with additional functionality """
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.propagate = False

    def setHandler(self, handler: logging.Handler) -> None:
        """
        Set handler for logger and ensures that this is the only handler assigned.

        Keep naming consistent with logging.Logger

        Args:
            handler (logging.Handler): Handler to set.
        """
        for handler in self.handlers:
            self.removeHandler(handler)
        self.addHandler(handler)


class StripAnsiFormatter(logging.Formatter):
    """ Formatter that strips ANSI formatting from log messages """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formatMessage(self, record: logging.LogRecord):
        record.msg = record.msg % record.args
        record.msg = strip_ansi(record.msg)
        message = self._fmt % record.__dict__
        return message


class ColoredFormatter(logging.Formatter):
    """ Formatter that adds ANSI color formatting to log messages, depending on their log level """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formatMessage(self, record: logging.LogRecord):
        record.msg = record.msg % record.args
        record.msg = strip_ansi(record.msg)
        
        message: str = {
            logging.DEBUG: lambda m: clicolor.cyan(m),
            logging.WARNING: lambda m: clicolor.yellow(m),
            logging.ERROR: lambda m: clicolor.red(m),
            logging.CRITICAL: lambda m: clicolor.red(m),
        }.get(record.levelno, lambda m: m)(self._fmt % record.__dict__)
        
        if message.startswith("INFO: "):
            message = message[6:]
        
        return message



def getLogger(name="") -> logging.Logger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    
    Args:
        name (str): Name of the logger to return.
        
    Returns:
        Logger: Logger with the specified name.
    """
    if not name or isinstance(name, str) and name == logging.root.name:
        return logging.root
    return Logger.manager.getLogger(name)
