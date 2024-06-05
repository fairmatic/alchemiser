# Monitoring

Library to publish statsd application metrics. 

To publish a new metrics,

1. Initialize an object of FMStatsd. 
    
    ```python
   from fmlib.monitoring import FMStatsd
   
   # For flask apps
   fmstatsd = LocalProxy(lambda: _fmstatsd)
   _fmstatsd: FMStatsd(env=os.getenv("ENV") or "dev")    
   
   fmstatsd = FMStatsd(env=os.getenv("ENV") or "dev")
    ```

2. Publish one of the supported metrics:
    ```python
    fmstatsd.gauge("metrics_name", value, tags={"application_id": application_id})
    ```
3. Use timing / incr decorators
    ```python
    from fmlib.monitoring import FMStatsd, fmstatsd_timing, fmstatsd_increment
   
    # Registering the fmstatsd object
    statsd_timing = partial(fmstatsd_timing, fmstatsd=fmstatsd)
    statsd_increment = partial(fmstatsd_increment, fmstatsd=fmstatsd)
   
   # Usage
   @statsd_timing(metric="service.heartbeat_consumer.timing")
   @statsd_increment(
       metric="some..metric", 
       value=1, 
       prepare_metric_tags=lambda x: ...
   )
   def foo(x):
      pass
    ```

## Quick local testing
```commandline
nc -u -l 9125
```

## Supported statsd metric types:

- decrement
- gauge
- histogram
- increment
- set
- timing
