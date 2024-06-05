# Exception Handler for Flask
import traceback

from flask import current_app as app
from werkzeug.exceptions import BadRequest

from fmlib.response import json_response


def handle_exceptions(error):
    """
    Handle different types of exceptions and return an appropriate error response.

    Args:
        error (Exception): An exception object that needs to be handled.

    Returns:
        tuple: A JSON response with the error message and a status code of 400.
    """
    app.logger.error(f"{error.__class__}: {error}")
    error_msg = "Something went wrong. Please try again."
    if isinstance(error, BadRequest):
        error_msg = "BadRequest: Invalid Request"
    elif isinstance(error, TypeError):
        error_msg = f"TypeError: {error}"
        app.logger.error(traceback.format_exc())
    elif isinstance(error, KeyError):
        error_msg = f"KeyError: {error}"
        app.logger.error(traceback.format_exc())
    return json_response(False, 400, None, error_msg)


def handle_500(error):
    app.logger.error(f"{error}")
    error_msg = "Something went wrong. Please try again."
    app.logger.error(traceback.format_exc())
    return json_response(False, 500, None, error_msg)


def handle_404(error):
    app.logger.error(f"{error}")
    error_msg = "Route Not Found."
    return json_response(False, 404, None, error_msg)


def handle_405(error):
    app.logger.error(f"{error}")
    error_msg = "Method Not Allowed"
    return json_response(False, 405, None, error_msg)


def handle_403(error):
    app.logger.error(f"{error}")
    error_msg = "Access Denied"
    return json_response(False, 403, None, error_msg)


def handle_401(error):
    app.logger.error(f"{error}")
    error_msg = "Unauthorized. Please login to access."
    return json_response(False, 401, None, error_msg)
