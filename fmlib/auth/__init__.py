from flask_cors import CORS
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    init,
)
from flask import Flask
from supertokens_python.recipe import (
    session,
    userroles,
)


def init_supertokens(service_name, api_domain, website_domain, super_tokens_connection_uri, super_tokens_api_key):
    """
    Initializes the Supertokens library for a Flask application.

    Args:
        service_name (str): The name of the service.
        api_domain (str): The domain of the API.
        website_domain (str): The domain of the website.
        super_tokens_connection_uri (str): The connection URI for Supertokens.
        super_tokens_api_key (str): The API key for Supertokens.

    Returns:
        None

    Example Usage:
        service_name: "your_service_name",
        api_domain: "your_api_domain",
        website_domain: "your_website_domain",
        super_tokens_connection_uri: "your_super_tokens_connection_uri",
        super_tokens_api_key: "your_super_tokens_api_key",
        setup_supertokens(service_name, api_domain, website_domain, super_tokens_connection_uri, super_tokens_api_key)
        
    """
    (
        init(
            app_info=InputAppInfo(
                app_name=service_name,
                api_domain=api_domain,
                website_domain=website_domain,
            ),
            supertokens_config=SupertokensConfig(
                connection_uri=super_tokens_connection_uri,
                api_key=super_tokens_api_key,
            ),
            framework="flask",
            recipe_list=[
                session.init(),  # initializes session features
                userroles.init(),
            ],
        ),
    )

def init_cors(app: Flask, origins: list[str] = None, headers: list[str] = []):
    """
    Initializes Cross-Origin Resource Sharing (CORS) for a Flask application.

    Args:
        app (Flask app): The Flask application object.
        origins (optional, list[str]): A list of allowed origins for CORS. If not provided, all origins are allowed.

    Example Usage:
        app = Flask(__name__)
        origins = ["https://example.com"]

        init_cors(app, origins)
    """

    allow_headers = ["Content-Type"] + headers
    CORS(app=app, origins=origins, allow_headers=allow_headers, supports_credentials=True)