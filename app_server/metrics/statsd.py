from werkzeug.local import LocalProxy

from fmlib.monitoring import FMStatsd

fmstatsd = LocalProxy(lambda: _fmstatsd)
_fmstatsd: FMStatsd = None


def init_fmstatsd(app):
    global _fmstatsd
    _fmstatsd = FMStatsd(
        env=app.config.get("ENV"),
        host=app.config.get("STATSD_HOST", "localhost"),
        port=app.config.get("STATSD_PORT", 9125),
    )
