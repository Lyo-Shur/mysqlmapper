from threading import Lock

_lock = Lock()


class Engine:
    """
    SQL Execution Engine
    """
    @staticmethod
    def query(conn, sql, parameter):
        """
        Query list information
        :param conn: Database connection
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        _lock.acquire()
        # ping check
        conn.ping(reconnect=True)
        # Get cursor
        cursor = conn.cursor()

        exception = None
        try:
            # Implementation of SQL
            cursor.execute(sql, parameter)
        except Exception as e:
            print(e)
            exception = e

        # Submit operation
        conn.commit()
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

    @staticmethod
    def count(conn, sql, parameter):
        """
        Query quantity information
        :param conn: Database connection
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        result = Engine.query(conn, sql, parameter)
        if len(result) == 0:
            return 0
        for value in result[0].values():
            return value

    @staticmethod
    def exec(conn, sql, parameter):
        """
        Execute SQL statement
        :param conn: Database connection
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        _lock.acquire()
        # ping check
        conn.ping(reconnect=True)
        # Get cursor
        cursor = conn.cursor()

        exception = None
        try:
            # Implementation of SQL
            cursor.execute(sql, parameter)
        except Exception as e:
            print(e)
            exception = e

        # Submit operation
        conn.commit()
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
