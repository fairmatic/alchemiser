"""
This module initializes and configures a Flask application. It registers namespaces and exception handlers, initializes the configuration, logging, Sentry, DB, and SuperTokens.
"""

from flask import Flask

from app_server import auth, config, db, exceptions, namespaces
from app_server.constants.env import Environment
from app_server.metrics.statsd import init_fmstatsd
from fmlib.fmlogger import FMLogger
from fmlib.sentry import setup_sentry

# Create the Flask app instance
app = Flask("SERVICENAME")


def register_exception_handlers(app: Flask) -> None:
    """
    Register exception handlers for the Flask app.

    Args:
        app (Flask): The Flask app instance.
    """
    app.register_error_handler(Exception, exceptions.handle_exceptions)
    app.register_error_handler(500, exceptions.handle_500)
    app.register_error_handler(404, exceptions.handle_404)
    app.register_error_handler(400, exceptions.handle_exceptions)
    app.register_error_handler(403, exceptions.handle_403)
    app.register_error_handler(401, exceptions.handle_401)


def initialize_config() -> config.Config:
    """
    Initialize the configuration for the application.

    Returns:
        Config: The initialized configuration for the application.

    Raises:
        ValueError: If the configuration is invalid or there is an error initializing the configuration.
    """
    try:
        # Create an instance of the Config class
        cfg = config.Config()

        # Validate the configuration
        cfg.validate()

        if cfg is not None:
            return cfg
        else:
            raise ValueError(f"Invalid Configuration: {cfg}")
    except Exception as e:
        raise ValueError(f"Error initializing configuration: {e}")


def create_app() -> Flask:
    """
    Configure and initialize a Flask application.

    Returns:
        app (Flask): The configured and initialized Flask app instance.
    """
    try:
        app.app_context().push()

        # Initialize extension objects
        app.logger.info("Initializing Configuration")
        cfg = initialize_config()
        app.config.from_object(cfg)

        # Configure logging
        app.logger.info("Initializing Logger")
        FMLogger.configure(log_level=cfg.LOG_LEVEL)

        # Register namespaces
        namespaces.init_namespaces()

        # Initialise  Namespaces
        namespaces.SERVICENAME_API.init_app(app)
        namespaces.init_namespaces()

        # Register exception handlers
        register_exception_handlers(app)

        # Initialise Sentry
        if (
            app.config.get("ENV") not in [None, Environment.DEVELOPMENT.value]
            and app.config.get("SENTRY_DSN") is not None
        ):
            app.logger.info("Initializing Sentry")
            setup_sentry(app.config.get("SENTRY_DSN", app.config.get("ENV")))

        # Initialise DB
        app.logger.info("Initializing DB")
        db.init_db(app)

        if app.config.get("ENV") == Environment.TEST.value:
            app.logger.info("Dropping and creating DB for testing")

            db.db.drop_all()
            db.db.create_all()

        # Initialise SuperTokens
        app.logger.info("Initializing SuperTokens")
        auth.setup_supertokens(app)

        # Initialise CORS
        app.logger.info("Initializing CORS")
        auth.setup_cors(app)

        # Initialise Statsd
        app.logger.info("Initializing Statsd")
        init_fmstatsd(app)

        return app

    except Exception:
        app.logger.exception("Unable to initialise app")
        raise ValueError("Error during app initialization")
