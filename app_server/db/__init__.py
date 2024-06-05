import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

metadata = MetaData()
Base = declarative_base(metadata=metadata)

db = None


def init_db(app: Flask):
    """
    Initialize the database manager with the given Flask app.

    Args:
        app (Flask): The Flask app instance.
    """
    try:
        global db
        if app and not db:
            db = SQLAlchemy(metadata=metadata)  # Note: Session needs to be committed explicitly
            db.init_app(app)
            if check_connection() is False:
                raise Exception("Unable to connect to database")
        elif not app:
            raise Exception("No Flask app instance provided")
        else:
            logging.info("Database already initialized")
    except Exception as e:
        logging.fatal(f"Error initializing database: {e}")
        raise e


def register_db():
    # Import and create models here
    # eg: from app.models import User, Post

    # Create tables if they don't exist
    pass


def create_db():
    # Create tables if they don't exist
    global db
    db.create_all()


def drop_db():
    global db
    db.drop_all()


def check_connection() -> bool:
    try:
        global db
        db.session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"errorYOLO {e}")
        logging.info("errorYOLO: %s", Exception.args)
        # logging.exception("Unable to connect to database to check connection")
        return False
