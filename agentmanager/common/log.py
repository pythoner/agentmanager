import logging
import logging.handlers

from agentmanager.util.conf import get_log_conf

ROOT_LEVEL = get_log_conf('logger_root', 'level')
LOG_FORMAT = get_log_conf('formatter_simpleFormatter', 'format')
DATE_FORMAT = get_log_conf('formatter_simpleFormatter', 'datefmt')
FILE_HANDLER_LEVEL = get_log_conf('handler_fileHandler', 'level')
FILE_HANDLER_PATH = get_log_conf('handler_fileHandler', 'path')
FILE_HANDLER_MODE = get_log_conf('handler_fileHandler', 'mode')
FILE_HANDLER_MAXBYTES = int(get_log_conf('handler_fileHandler', 'maxbytes'))
FILE_HANDLER_BACKUPCOUNT = int(get_log_conf('handler_fileHandler',
                                            'backupcount'))
CONSOLE_HANDLER_LEVEL = get_log_conf('handler_consoleHandler', 'level')


class ContextAdapter:
    def __init__(self, logger):
        self.logger = logger

    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)

    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)

    def warning(self, msg):
        if msg is not None:
            self.logger.warning(msg)

    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)

    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)

_loggers = {}


def logger(name='unknown'):
    if name not in _loggers:
        _loggers[name] = ContextAdapter(logging.getLogger(name))
    return _loggers[name]


def InitLog(file_name):
    initlogger = logger(None).logger
    initlogger.setLevel(getattr(logging, ROOT_LEVEL))
    filepath = FILE_HANDLER_PATH + '/' + file_name
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler = logging.handlers.WatchedFileHandler(
        filename=filepath,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, FILE_HANDLER_LEVEL))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, CONSOLE_HANDLER_LEVEL))
    console_handler.setFormatter(formatter)
    initlogger.addHandler(file_handler)
    initlogger.addHandler(console_handler)
