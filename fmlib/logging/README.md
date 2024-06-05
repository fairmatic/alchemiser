fmlib logging [Deprecated]
=============

## Overview
This logging will be deprecated soon. Please start using `fmlogger` package from fmlib.


## Usage/Examples of fmlogger

```python
from fmlib.logger import FMLogger

FMLogger.configure()
# Always initialize logger with __name__ of the module.
logger = FMLogger.logger(__name__)

logger.info('This is a log message', client_ip='172.32.61.99', foo='bar')
```

This gives output as follows:
```
{"message": "This is a log message", "fields": {"client_ip": "172.32.61.99", "foo": "bar", "loc": "/Users/ayush/Work/Repos/test_logging/test.py:7", "thread": 140704614430464, "threadName": "MainThread", "process": 89985, "processName": "MainProcess", "logger": "__main__", "module": "test", "funcName": "<module>"}, "timestamp": "2023-11-20T13:14:05.027+0530", "log_level": "INFO"}
```
