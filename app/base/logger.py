import flask
import itertools
import json
import traceback
import logging
from logging import handlers

from flask import logging as flask_logging


def config_logger(service):

    logging.setLoggerClass(UbiomeLogger)

    # Log SQLAlchemy on DEBUG mode
    if service.config['DEBUG'] == 'True':
        logging.captureWarnings(True)
        sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
        sqlalchemy_logger.addHandler(logging.StreamHandler())

        log_handler = logging.StreamHandler()
        log_handler.setLevel(service.config.get('LOGGING_LEVEL'))
        log_handler.setFormatter(logging.Formatter(flask_logging.DEBUG_LOG_FORMAT))
        service.logger.addHandler(log_handler)
    else:
        werkzeug_log = logging.getLogger('werkzeug')
        werkzeug_log.disabled = True
        del service.logger.handlers[:]

        log_handler = handlers.RotatingFileHandler(maxBytes=service.config.get('LOGGING_MAXBYTES', 100000000),
                                           backupCount=service.config.get('LOGGING_BKP_COUNTS', 10),
                                           filename=service.config['TEXT_LOGGING_LOCATION'])
        log_handler.setLevel(service.config.get('LOGGING_LEVEL'))
        log_handler.setFormatter(logging.Formatter(flask_logging.PROD_LOG_FORMAT))
        service.logger.addHandler(log_handler)

        json_handler = handlers.RotatingFileHandler(maxBytes=service.config.get('LOGGING_MAXBYTES', 100000000),
                                           backupCount=service.config.get('LOGGING_BKP_COUNTS', 10),
                                           filename=service.config['JSON_LOGGING_LOCATION'])
        json_handler.setLevel(service.config.get('LOGGING_LEVEL'))
        json_handler.setFormatter(JSONFormatter())
        service.logger.addHandler(json_handler)


class JSONFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record):
        msg = {"name": "ubiome-orders-api",
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "levelno": record.levelno,
            "message": record.getMessage(),

            "msecs": record.msecs,

            "filename": record.filename,
            "funcname": record.funcName,
            "lineno": record.lineno
        }

        if hasattr(record, 'extra'):
            msg["extra"] = record.extra

        return json.dumps(msg)

    def _formatException(self, ei, strip_newlines=True):
        lines = traceback.format_exception(*ei)
        if strip_newlines:
            lines = [itertools.ifilter(lambda x: x, line.rstrip().splitlines())
                     for line in lines]
            lines = list(itertools.chain(*lines))
        return lines


class UbiomeLogger(logging.Logger):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        """
        We only check if any key in extra dict is duplicated with the keys that exist already in the record.
        Otherwise we append the extra parameter as a new entry in the dictionary
        Also we add the user id and request id to the log message if they exist in flask.g local thread
        """
        if isinstance(msg, dict):
            msg = json.dumps(msg)

        rv = logging.LogRecord(name, level, fn, lno, msg, args, exc_info, func)
        if extra is not None:
            for key in list(extra):
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                if extra.get(key) is None:
                    extra.pop(key)
            rv.__dict__['extra'] = extra
        else:
            extra = dict()


        if hasattr(flask.g, 'user'):
            extra['user_id'] = str(flask.g.user.id)
            msg = "User %s :: %s" % (flask.g.user.id, msg)
        if hasattr(flask.g, 'request_id'):
            extra['request_id'] = flask.g.request_id
            msg = "Request ID %s :: %s" % (flask.g.request_id, msg)

        rv.msg = msg
        return rv
