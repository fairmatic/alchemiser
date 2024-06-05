import os
import time

import logging
import logging.config
import socket

from pythonjsonlogger import jsonlogger


class FMLoggerAdapter(logging.LoggerAdapter):
    """
    FM Style logger adapter to support structured logging
    """
    def process(self, msg, kwargs):
        fields = {'extra': {'fields': kwargs}}
        fields['exc_info'] = kwargs.get('exc_info', False)
        return msg, fields


class FMJsonLogFormatter(jsonlogger.JsonFormatter):
    """
    FM Style JSON Log Formatter
    """

    default_msec_format = '%s.%03d'

    def add_fields(self, log_record, record, message_dict):
        super(FMJsonLogFormatter, self).add_fields(log_record, record, message_dict)
        self._enrich_with_metadata(log_record, record)
        self._enrich_for_exception(log_record, record)

    def _enrich_with_metadata(self, log_record, record):
        """
        Add additional metadata fields in log record
        """
        meta_fields = {
            'loc':         f"{record.pathname}:{record.lineno}",
            'thread':      record.thread,
            'threadName':  record.threadName,
            'process':     record.process,
            'processName': record.processName,
            'logger':      record.name,
            'module':      record.module,
            'funcName':    record.funcName,
        }

        log_record['fields'] = log_record.get('fields', {})
        log_record['fields'].update(meta_fields)

    def _enrich_for_exception(self, log_record, record):
        """
        Add exception info in the log if 'exc_info' is set to True
        """
        if log_record.get('exc_info', False):
            log_record['stack_trace'] = log_record.pop('exc_info')
            log_record['exception_class'] = record.exc_info[0].__name__
            log_record['exception_message'] = record.exc_info[1]


    def formatTime(self, record, datefmt=None):
        """
        Override formatTime to add milliseconds to the timestamp and support %F in datefmt
        """
        ct = self.converter(record.created)
        if datefmt:
            if "%F" in datefmt:
                msec = "%03d" % record.msecs
                datefmt = datefmt.replace("%F", msec)
                s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s,%03d" % (t, record.msecs)
        return s


class FMLogger:
    """
    Helper class to configure and use FM Style logger
    """
    @staticmethod
    def configure(log_level=logging.INFO):
        """
        Call this method to configure the global logger
        """
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    '()': FMJsonLogFormatter,
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'rename_fields': {'asctime': 'timestamp', 'levelname': 'log_level'},
                    # Log timestamps in ISO 8601/RFC 3339 style
                    'datefmt': "%Y-%m-%dT%H:%M:%S.%F%z",
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json',
                    'stream': 'ext://sys.stdout',
                },
            },
            'root': {
                'propogate': False,
                'level': log_level,
                'handlers': ['console'],
            },
        }

        config = FMLogger._enable_vector_logging(config)

        logging.config.dictConfig(config)

    @staticmethod
    def _enable_vector_logging(config):
        # Send json logs to vector
        VECTOR_LOGS_ENABLED = os.getenv('VECTOR_LOGS_ENABLED', default=False)
        VECTOR_HOST = os.getenv('VECTOR_HOST', default='localhost')
        VECTOR_PORT = os.getenv('VECTOR_PORT', default='9514')


        if VECTOR_LOGS_ENABLED:
            vector_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            vector_udp_socket.connect((VECTOR_HOST, int(VECTOR_PORT)))
            vector_udp_socket_stream = vector_udp_socket.makefile('w')

            vector_logging = {
              'class': 'logging.StreamHandler',
              'formatter': 'json',
              'stream': vector_udp_socket_stream,
            }

            config['handlers']['vector'] = vector_logging
            config['root']['handlers'].append('vector')

        return config

    @staticmethod
    def logger(namespace=None):
        """
        Call this method to get a logger instance which supports structured logging
        """
        logger = logging.getLogger(namespace)
        return FMLoggerAdapter(logger, {})

