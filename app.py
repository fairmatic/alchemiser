# Main application file for the SERVICENAME application. This file is the entry point for the application and is responsible for creating the application instance and running the application.
import logging

from flask_migrate import Migrate

from app_server import create_app
from app_server.db import db

SERVICENAME = create_app()
migrate = Migrate(SERVICENAME, db)


def main():
    """Main function to run the application."""
    try:
        logging.info("Starting the application...")
        SERVICENAME.run(host="::", port=5000)
    except Exception as e:
        logging.fatal(f"Failed to start the application: {e}")


if __name__ == "__main__":
    main()
