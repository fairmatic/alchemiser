bind = "0.0.0.0:5000"

backlog = 2048  #  The maximum number of pending connections. This refers to the number of clients that can be waiting to be served. Exceeding this number results in the client getting an error when attempting to connect. It should only affect servers under significant load.
workers = 4  # The number of worker processes for handling requests. A positive integer generally in the 2-4 x $(NUM_CORES) range. You'll want to vary this a bit to find the best for your particular application's work load.
worker_class = "gevent"  # The type of workers to use. The default class (sync) should handle most 'normal' types of workloads. You'll want to read http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type to understand the implications of the various choices.
worker_connections = 100  # The maximum number of simultaneous clients.
timeout = 90  # Workers silent for more than this many seconds are killed and restarted.
keepalive = 60  # The number of seconds to wait for requests on a Keep-Alive connection.
graceful_timeout = 60  # The maximum time to wait for pending connections to finish during a restart.
statsd_host = "localhost:9125"  # The host and port of the statsd server to send metrics to.

errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

pidfile = "gunicorn_pid"
daemon = (
    False
)  # Daemonize the Gunicorn process. Detaches the server from the controlling terminal and enters the background.

disable_existing_loggers = True  # If true, Gunicorn will not configure the logging system. This means that log settings will have to be applied via the logging module.


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    server.log.info("Worker is spawning (pid: %s)", worker.pid)
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import sys
    import threading
    import traceback

    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])  # noqa
    code = []
    for threadId, stack in list(sys._current_frames().items()):
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
