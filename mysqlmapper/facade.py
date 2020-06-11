from tabledbmapper.facade import Engine, TableDBMapper, MVC

from mysqlmapper.engine import MysqlEngine
from mysqlmapper.manager.mvc.holder import MVCHolder
from mysqlmapper.manager.info import get_db_info


class Mysql(Engine):
    """
    MYSQL Execution Engine
    """
    @staticmethod
    def get_engine(host, user, password, database, charset="utf8"):
        """
        Init SQL Execution Engine
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        return MysqlEngine(host, user, password, database, charset)


class Database:
    """
    Summary of database info operations
    """
    @staticmethod
    def get_info(conn, database_name):
        """
        Get database information
        :param conn: Database connection
        :param database_name: Database name
        :return: database information
        """
        return get_db_info(conn, database_name)


class MysqlMVC(MVC):
    """
    Summary of MVCHolder operations
    """
    @staticmethod
    def get_holder(host, user, password, database, charset="utf8"):
        """
        Initialize MVC holder
        :param host: host name
        :param user: User name
        :param password: Password
        :param database: Database name
        :param charset: Encoding format
        """
        return MVCHolder(host, user, password, database, charset)


class MysqlMapper(TableDBMapper):
    """
    Summary of common operations
    """
    # MYSQL Execution Engine
    Engine = Mysql
    # MVC
    MVC = MysqlMVC
    # Database info
    Database = Database
