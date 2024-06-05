from datetime import datetime, timedelta, timezone

import jwt
from flask.testing import FlaskClient
from flask_testing import TestCase

from app_server.db import db


class BaseTest(TestCase):
    """
    A test case class that provides common functionalities and setup for testing Flask applications.

    Attributes:
        app: The Flask application object.
        client: The Flask test client object.
        jwt_token: The JWT token generated with a positive time delta.
        jwt_token_expired: The JWT token generated with a negative time delta, representing an expired token.
    """

    def __init__(self):
        """
        Initializes the BaseTest class by creating the Flask application, test client, and generating JWT tokens.
        """
        self.app = self.create_app()
        self.client = self.get_client()
        self.jwt_token = self.get_jwt_token()
        self.jwt_token_expired = self.get_jwt_token(time_delta=-1)

    def create_app(self):
        """
        Creates and returns the Flask application.

        Returns:
            The Flask application object.
        """
        app = self.get_app()
        return app

    @staticmethod
    def get_jwt_token(self, time_delta=1):
        """
        Generates a JWT token with an expiration time based on the current time and a time delta.

        Args:
            time_delta: The time delta in days for the expiration time. Default is 1 day.

        Returns:
            The generated JWT token.
        """
        jwt_token = jwt.encode(
            {"email": "test@fairmatic.com", "exp": datetime.now(tz=timezone.utc) + timedelta(days=time_delta)},
            secret=self.app.config.get("JWT_SECRET"),
            algorithm=self.app.config.get("JWT_ALGORITHM"),
        )
        return jwt_token

    @staticmethod
    def get_app():
        """
        Creates and returns the Flask application.

        Returns:
            The Flask application object.
        """
        from app_server import create_app

        app = create_app()
        return app

    def get_client(self):
        """
        Creates and returns a Flask test client.

        Returns:
            The Flask test client object.
        """
        return FlaskClient(
            application=self.app,
            response_wrapper=self.app.response_class,
        )

    @staticmethod
    def setup_db(self):
        """
        Sets up the database by initializing it and executing necessary SQL statements.
        """
        db.session.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    def tearDown(self):
        """
        Tears down the database session.
        """
        db.session.remove()
