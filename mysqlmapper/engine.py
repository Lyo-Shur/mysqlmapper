import pymysql
from tabledbmapper.engine import ExecuteEngine, ConnHandle, QueryResult, CountResult, ExecResult, ConnBuilder, \
    TemplateEngine
from tabledbmapper.logger import Logger


class MySQLConnBuilder(ConnBuilder):

    host = None
    user = None
    password = None
    database = None
    charset = None

    def __init__(self, host: str, user: str, password: str, database: str, charset="utf8"):
        """
        Init MySQL Conn Handle
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def connect(self) -> pymysql.Connection:
        """
        Gets the database connection method
        """
        return pymysql.connect(
            host=self.host,
            user=self.user, password=self.password,
            database=self.database,
            charset=self.charset)


class MySQLConnHandle(ConnHandle):

    def ping(self, conn: pymysql.Connection):
        """
        Test whether the connection is available, and reconnect
        :param conn: database conn
        """
        conn.ping(reconnect=True)

    def commit(self, conn: pymysql.Connection):
        """
        Commit the connection
        :param conn: database conn
        """
        conn.commit()

    def rollback(self, conn: pymysql.Connection):
        """
        Rollback the connection
        :param conn: database conn
        """
        conn.rollback()


class MySQLExecuteEngine(ExecuteEngine):
    """
    MySQL Execution Engine
    """
    def query(self, conn: pymysql.Connection, logger: Logger, sql: str, parameter: list) -> QueryResult:
        """
        Query list information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        exception = None
        try:
            logger.print_info(sql, parameter)
            cursor.execute(sql, parameter)
        except Exception as e:
            logger.print_error(e)
            cursor.close()
            raise exception

        # get result
        result = cursor.fetchall()
        # Close cursor
        cursor.close()
        return result

    def count(self, conn: pymysql.Connection, logger: Logger, sql: str, parameter: list) -> CountResult:
        """
        Query quantity information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        result = self.query(conn, logger, sql, parameter)
        if len(result) == 0:
            return 0
        for value in result[0].values():
            return value

    def exec(self, conn: pymysql.Connection, logger: Logger, sql: str, parameter: list) -> ExecResult:
        """
        Execute SQL statement
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        cursor = conn.cursor()

        exception = None
        try:
            logger.print_info(sql, parameter)
            cursor.execute(sql, parameter)
        except Exception as e:
            logger.print_error(e)
            cursor.close()
            raise exception

        # Number of rows affected
        rowcount = cursor.rowcount
        # Last insert ID
        lastrowid = cursor.lastrowid
        # Close cursor
        cursor.close()
        return lastrowid, rowcount


class MySQLTemplateEngine(TemplateEngine):
    def __init__(self, conn: pymysql.Connection):
        super().__init__(MySQLConnHandle(), MySQLExecuteEngine(), conn)
