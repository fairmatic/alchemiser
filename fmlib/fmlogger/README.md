fmlib logging
=============

## Overview

fmlib logging class is designed to emit a json style log adhering to format
decided in the [Log Management proposal document](https://fairmatic.atlassian.net/l/cp/n163y5aj)

The expectation is to have log format that looks like following to reduce log
parsing, enriching by log shipper. We are calling this FM Style log format.

```json
{
  "timestamp": "ISO8601_format_time with timzone in UTC",
  "message": "<log_message>",
  # This is for extracted fields from message. (Optional)
  "fields": {
    "client_IP": "174.195.133.212",
    "loc": "<file_path>:<line_number>",
    ...
  },
  "log_level": "<INFO/DEBUG/ERROR>"
  "tags": {
    "service": "<service_name>",
    "repo": "<repository_name>",
    "version": "<git_sha>",
    "env": "<prod/test/stage>",
    "deployment": "<ECS/lambda/EMR>",
    "host": "<host_name>",
    ...
  }
}
```

This log format supports structured log formatting, where structured log fields
are to be inserted in the `fields` key.

Please note that the `tags` key is designed to be enriched by log shipper to add
additional info on the service environment. It is not responsiblity of the the
logging library.

## Usage

This module provides `FMLogger` helper class to configure logging configuration
which follows FM Logging Style and also adds a utility function to get logger
with adapter to support structured logging.

### Configure logger
You can configure logs format by following invocation.

Please note that you require to call this only once during initialization of
your application. It will reset the configuration to fmlib defaults.

#### Initialize FMLogger config
```python
from fmlib.fmlogger import FMLogger

# Set log format to FM Style Log format. Defaults to INFO log_level
FMLogger.configure()

# Or Configure FM Style Log format with DEBUG log_level
FMLogger.configure(log_level='DEBUG')
```

Configuration this will set the log format of any external library using the
internal logging module to FM Style log as well.


### Using structured logging facility
You can log by initializing the logger with `FmLogger.logger()`. This logger is
a thin wrapper around python's internal logging module. The logger created this
way also supports supports structured logging. Any key, value argument added to
the logger will be added in the `fields` key of the json log output. key.

#### Example:

```python
from fmlib.fmlogger import FMLogger

FMLogger.configure()
# Always initialize logger with __name__ of the module.
logger = FMLogger.logger(__name__)

logger.info('This is a log message', client_ip='172.32.61.99', foo='bar')
```

This gives output as follows:
```
{"message": "This is a log message", "fields": {"client_ip": "172.32.61.99", "foo": "bar", "loc": "/Users/ayush/Work/Repos/test_logging/test.py:7", "thread": 140704614430464, "threadName": "MainThread", "process": 89985, "processName": "MainProcess", "logger": "__main__", "module": "test", "funcName": "<module>"}, "timestamp": "2023-11-20T13:14:05.027+0530", "log_level": "INFO"}
```
