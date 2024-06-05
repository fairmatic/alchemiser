"""Utilities for generating JSON responses for APIs."""

import json
import decimal
from flask import Response
import simplejson as json
import datetime


JSON_CONTENT_TYPE = "application/json"
class CustomEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that provides serialization for specific types of objects.

    Inherits from `json.JSONEncoder` and overrides the `default` method to handle `datetime.datetime`,
    `datetime.date`, and `decimal.Decimal` objects and convert them to ISO format.

    Raises:
        TypeError: If the object is not an instance of `datetime.datetime`, `datetime.date`, or `decimal.Decimal`.

    Example Usage:
        # Create an instance of CustomEncoder
        encoder = CustomEncoder()

        # Serialize an object using the custom encoder
        data = {"date": datetime.datetime.now(), "amount": decimal.Decimal("10.50")}
        json_data = json.dumps(data, cls=encoder)

        print(json_data)
    """

    def default(self, obj):
        """
        Convert the given object to a JSON serializable format.

        Args:
            obj: The object to be serialized.

        Returns:
            str: The serialized object in ISO format.

        Raises:
            TypeError: If the object is not an instance of `datetime.datetime`, `datetime.date`, or `decimal.Decimal`.
        """
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, (datetime.date, decimal.Decimal)):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex

        raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")

def json_response(success: bool, status_code, data=None, err_message=None):
    """
    Generate a JSON response.

    Args:
        success (bool): Indicates if the response is successful.
        status_code: The status code of the response.
        data: The data to include in the response.
        err_message: The error message to include in the response if success is False.
        error_code: The error code to include in the response if success is False.

    Returns:
        The JSON response.

    Raises:
        ValueError: If data is not JSON serializable.
    
    Example Usage:
        # Generate a successful response
        json_response(success=True, status_code=200, data={"message": "Success!"})

        # Generate an error response
        json_response(success=False, status_code=400, err_message="Error!")
    """
   
    body = {}
    body["success"] = success
    body["code"] = status_code

    if not success:
        if err_message is not None:
            body["error"] = {"message": err_message}

    if data:
        if isinstance(data, (list, dict, str, int, float, bool, type(None))):
            body["data"] =data
        else:
            raise ValueError("data is not JSON serializable")
    
    if not data:
        body["data"] = {}
        
    response = Response(status=status_code,
                        mimetype=JSON_CONTENT_TYPE, response=json.dumps(body, cls=CustomEncoder))
    response.headers["Content-Type"] = JSON_CONTENT_TYPE

    return response
