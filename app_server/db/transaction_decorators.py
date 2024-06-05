from contextlib import contextmanager
from functools import wraps

from app_server.db import db


@contextmanager
def db_transaction():
    """
    Use this method to wrap a function that needs to be executed in a transaction. If the function is already in a
    transaction, then the function will be executed without starting a new transaction and be executed as a part of the
    existing transaction. If the function is not in a transaction, then a new transaction will be started and the
    function will be executed in that transaction.
    :return:
    """

    start_transaction = not db.session.is_active
    if start_transaction:
        with db.session.begin():
            yield
    else:
        yield


def db_transactional(func):
    """
    Decorator that wraps a function with a database transaction.

    Args:
        func: The function to be decorated with a database transaction.

    Returns:
        The wrapped version of the original function.

    Example Usage:
        @db_transactional
        def update_user(user_id, new_data):
            # Update user data in the database
            ...

        update_user(123, {"name": "John Doe"})
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        with db_transaction():
            result = func(*args, **kwargs)
        return result

    return decorated_function
