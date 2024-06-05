import os
from typing import Dict, Optional

from datadog.dogstatsd.base import DogStatsd

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9125


class FMStatsd(object):

    _supported_statsd_methods = [
        "decrement",
        "gauge",
        "histogram",
        "increment",
        "set",
        "timing",
    ]

    def __init__(self, env, host=None, port=None, enabled=None):
        """
        Initializes FMStatsd Object.
        @param env: service environment, e.g. prod, dev, stage, etc. By default, disabled for dev and test envs.
        @param host: dogstatsd host. STATSD_HOST env variable gets priority over this.
                    If both are not set, 'localhost' will be used.
        @param port: dogstatsd port. STATSD_PORT env variable gets priority over this.
                    If both are not set, '9125' will be used.
        @param enabled: If True, will be enabled in all envs, if False, will be disabled in all envs
        """
        self.enabled = enabled

        assert env, "Missing environment"
        self.env = env

        self.use_ms = True

        host = os.getenv("STATSD_HOST") or host or DEFAULT_HOST
        port = os.getenv("STATSD_PORT") or port or DEFAULT_PORT

        self.dstatsd = DogStatsd(host=host, port=port, use_ms=self.use_ms, namespace="fm")

    def timing(self, key, val, **kwargs):
        """
        Note:
        1. For all the time related metrics, we are sending metric value in seconds from code and relying on
        use_ms flag for conversion to ms, inside the DogStatsd class.
        2. DogStatsd implementation of this method has value unit hardcoded as ms, this override is to send value
        in ms or seconds depending on use_ms flag.
        """
        kwargs = self._check_env_and_mandatory_tags(kwargs)
        if kwargs:
            val = val if not self.use_ms else int(round(1000 * val))
            self.dstatsd.timing(key, val, **kwargs)
        else:
            return

    def _check_env_and_mandatory_tags(self, o: Dict) -> Optional[Dict]:
        """
        Checks env and Adds current env in the tags.
        Use enabled to override env check, for e.g. testing metrics locally in dev environment

        @param o: dictionary of tags
        @return: modified list of tags in dogstatsd format
        """
        if self.enabled is False or (self.enabled is None and self.env in ["dev", "test"]):
            return None
        elif (self.enabled is None) or (self.enabled is True):
            tags = o.get("tags", {})
            assert isinstance(tags, dict)
            tags["env"] = self.env
            # convert to the dogstatsd-accepted format of a list of strings
            # converting value to lower case for consistency
            o["tags"] = [f"{str(k)}:{str(v).lower()}" for k, v in tags.items()]
            return o
        else:
            return None

    def __getattr__(self, name):
        def decorated_method(*args, **kwargs):
            kwargs = self._check_env_and_mandatory_tags(kwargs)
            if not kwargs:
                return
            else:
                return attr(*args, **kwargs)

        if name in FMStatsd._supported_statsd_methods:
            attr = getattr(self.dstatsd, name)
            if hasattr(attr, "__call__"):
                return decorated_method
            else:
                return attr
        else:
            raise AttributeError(
                f"Attribute {name} not supported or does not exist in Dstatsd client"
            )
