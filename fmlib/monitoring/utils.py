import timeit
from functools import wraps
from typing import Callable, Optional

from ..fmlogger import FMLogger

log = FMLogger.logger(__name__)

def fmstatsd_timing(fmstatsd, metric, prepare_metric_tags: Optional[Callable] = None):
    """
    @param fmstatsd: FMStatsd object
    @param metric: the metric to apply the FMStatsd function on
    @param prepare_metric_tags: A callable to prepare the tags if any
    """
    def decorator(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            tags = prepare_metric_tags(*args, **kwargs) if prepare_metric_tags else {}
            start_time = timeit.default_timer()
            result = f(*args, **kwargs)
            try:
                elapsed_seconds = timeit.default_timer() - start_time
                fmstatsd.timing(metric, elapsed_seconds, **tags)
            except Exception:
                log.error(f"Statsd Error :: Timing Decorator")
            return result
        return _wrapper
    return decorator


def fmstatsd_increment(fmstatsd, metric, value, prepare_metric_tags: Optional[Callable] = None):
    """
    @param fmstatsd: FMStatsd object
    @param metric: the metric to apply the FMStatsd function on
    @param prepare_metric_tags: A callable to prepare the tags if any
    """
    def decorator(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            tags = prepare_metric_tags(*args, **kwargs) if prepare_metric_tags else {}
            result = f(*args, **kwargs)
            try:
                fmstatsd.increment(metric=metric, value=value, tags=tags)
            except Exception:
                log.error(f"Statsd Error :: Increment Decorator")
            return result
        return _wrapper
    return decorator
