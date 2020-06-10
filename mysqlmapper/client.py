import pymysql


class ConnHolder:
    """
    Database connection holder
    """

    # Database connection
    _conn = None

    def __init__(self, host, user, password, database, charset="utf8"):
        """
        Initialize database connection
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        self._conn = pymysql.connect(
            host=host,
            user=user, password=password,
            database=database,
            charset=charset)

    def get_conn(self):
        """
        Get database connection
        :return: Database connection
        """
        return self._conn
