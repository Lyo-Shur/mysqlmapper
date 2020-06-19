from threading import Lock

import pymysql
from tabledbmapper.engine import Engine

_lock = Lock()


class MysqlEngine(Engine):
    """
    MYSQL Execution Engine
    """
    def __init__(self, host, user, password, database, charset="utf8"):
        """
        Init SQL Execution Engine
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        super().__init__(host, user, password, database, charset)
        self._conn = pymysql.connect(
            host=host,
            user=user, password=password,
            database=database,
            charset=charset)

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
            # Submit operation
            self._conn.commit()
            # Close cursor
            cursor.close()
            _lock.release()
            raise exception

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
            # Submit operation
            self._conn.commit()
            # Close cursor
            cursor.close()
            _lock.release()
            raise exception

        # Submit operation
        self._conn.commit()
        # Number of rows affected
        rowcount = cursor.rowcount
        # Last insert ID
        lastrowid = cursor.lastrowid
        # Close cursor
        cursor.close()
        _lock.release()
        return lastrowid, rowcount
