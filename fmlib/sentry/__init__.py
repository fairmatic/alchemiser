# Initialise Sentry
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def setup_sentry(sentry_dsn, env) -> None:
    """
    Initializes the Sentry SDK for error monitoring and performance monitoring in a Flask application.

    Args:
        config (dict): A dictionary containing the configuration values for the Sentry SDK. It should have the `SENTRY_DSN` and `env` keys.

    Returns:
        None

    Example Usage:
        
        sentry_dsn: "your_sentry_dsn",
        env: "production"
        init_sentry(config)
    """
    sentry_dsn = sentry_dsn
    assert sentry_dsn
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.0,  # disabling the apm
        integrations=[FlaskIntegration()],
        # By default, the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        # release="myapp@1.0.0",
        environment=env,
    )
