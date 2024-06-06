from flask import Flask

from fmlib.auth import init_cors, init_supertokens


def setup_supertokens(app):
    """
    Initializes the Supertokens library for a Flask application.

    Args:
        app (Flask app): The Flask application object.

    Example Usage:
        app = Flask(__name__)
        app.config["SERVICE_NAME"] = "my_service"
        app.config["API_DOMAIN"] = "api.example.com"
        app.config["WEBSITE_DOMAIN"] = "example.com"
        app.config["SUPER_TOKENS_CONNECTION_URI"] = "https://supertokens.io"
        app.config["SUPER_TOKENS_API_KEY"] = "my_api_key"

        setup_supertokens(app)

    This function initializes the Supertokens library for a Flask application by retrieving the necessary configuration values from the Flask application object and passing them to the `init_supertokens` function.
    """

    service_name = app.config.get("SERVICE_NAME")
    api_domain = app.config.get("API_DOMAIN")
    website_domain = app.config.get("WEBSITE_DOMAIN")
    connection_uri = app.config.get("SUPER_TOKENS_CONNECTION_URI")
    api_key = app.config.get("SUPER_TOKENS_API_KEY")
    # init_supertokens(service_name, api_domain, website_domain, connection_uri, api_key)


def setup_cors(app: Flask, origins: list[str] = None):
    """
    Initializes CORS for a Flask application.

    Args:
        app (Flask app): The Flask application object.
        origins (optional, list[str]): A list of allowed origins for CORS. If not provided, it will be fetched from the Flask application configuration under the key "CORS_ORIGIN".
    """
    origins = app.config.get("CORS_ORIGIN") if origins is None else origins
    init_cors(app, origins)
