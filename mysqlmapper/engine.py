from threading import Lock

from mysqlmapper.logger import DefaultLogger
from mysqlmapper.sql_builder import builder

_lock = Lock()


class Engine:
    """
    SQL Execution Engine
    """

    # Database connection
    _conn = None

    # Logger
    _logger = None

    def __init__(self, conn):
        """
        Init SQL Execution Engine
        :param conn: Database connection
        """
        self._conn = conn
        self._logger = DefaultLogger()

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._logger = logger
        return self

    def query(self, sql, parameter):
        """
        Query list information
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        _lock.acquire()
        # ping check
        self._conn.ping(reconnect=True)
        # Get cursor
        cursor = self._conn.cursor()

        exception = None
        try:
            # logger
            self._logger.print_info(sql, parameter)
            # Implementation of SQL
            cursor.execute(sql, parameter)
        except Exception as e:
            self._logger.print_error(e)
            exception = e

        # Submit operation
        self._conn.commit()
        # Get table header
        names = []
        for i in cursor.description:
            names.append(i[0])
        # Get result set
        results = []
        for i in cursor.fetchall():
            result = {}
            for j in range(len(i)):
                result[names[j]] = i[j]
            results.append(result)
        cursor.close()
        _lock.release()

        # Delay throw exception
        if exception is not None:
            raise exception
        return results

    def count(self, sql, parameter):
        """
        Query quantity information
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        result = self.query(sql, parameter)
        if len(result) == 0:
            return 0
        for value in result[0].values():
            return value

    def exec(self, sql, parameter):
        """
        Execute SQL statement
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        _lock.acquire()
        # ping check
        self._conn.ping(reconnect=True)
        # Get cursor
        cursor = self._conn.cursor()

        exception = None
        try:
            # logger
            self._logger.print_info(sql, parameter)
            # Implementation of SQL
            cursor.execute(sql, parameter)
        except Exception as e:
            self._logger.print_error(e)
            exception = e

        # Submit operation
        self._conn.commit()
        # Number of rows affected
        rowcount = cursor.rowcount
        # Last insert ID
        lastrowid = cursor.lastrowid
        # Close cursor
        cursor.close()
        _lock.release()

        # Delay throw exception
        if exception is not None:
            raise exception
        return lastrowid, rowcount


class TemplateEngine:
    """
    SQL template execution engine
    Using the jinja2 template engine
    """

    # SQL Execution Engine
    _engine = None

    def __init__(self, conn):
        """
        Init SQL Execution Engine
        :param conn: Database connection
        """
        self._engine = Engine(conn)

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._engine.set_logger(logger)
        return self

    def query(self, sql_template, parameter):
        """
        Query list information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.query(sql, param)

    def count(self, sql_template, parameter):
        """
        Query quantity information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.count(sql, param)

    def exec(self, sql_template, parameter):
        """
        Execute SQL statement
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.exec(sql, param)
