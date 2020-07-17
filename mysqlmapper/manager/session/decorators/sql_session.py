from functools import wraps
from typing import Callable, Dict

from mysqlmapper.manager.session.sql_session_factory import MySQLSessionFactory


SessionResult = Dict


# Add a decorator to the method to automatically open the session when you enter the method
def mapper(factory: MySQLSessionFactory) -> Callable:
    # Gets the session factory location
    @wraps(factory)
    def decorator(func):
        # Method to add a decorator
        @wraps(func)
        def wrapper(*args, **kwargs) -> SessionResult:
            params = [factory.get_common_session()]
            for arg in args:
                params.append(arg)
            new_args = tuple(params)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator
