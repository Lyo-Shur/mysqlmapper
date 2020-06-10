from mysqlmapper.manager.mvc.holder import MVCHolder
from mysqlmapper.sql_builder import builder
from mysqlmapper.client import ConnHolder
from mysqlmapper.engine import Engine, TemplateEngine
from mysqlmapper.manager.info import get_db_info
from mysqlmapper.manager.manager import Manager as Manage
from mysqlmapper.manager.xml_config import parse_config_from_string, parse_config_from_file


class Conn:
    """
    Summary of database init operations
    """
    @staticmethod
    def get_holder(host, user, password, database, charset="utf8"):
        """
        Initialize database connection
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        :return: ConnHolder
        """
        return ConnHolder(host, user, password, database, charset)


class Builder:
    """
    Summary of builder operations
    """
    @staticmethod
    def sql_builder(template, parameter):
        """
        Build SQL string
        :param template: Init jinja2 template
        :param parameter: Parameter
        :return: Jinja2 template return
        """
        return builder(template, parameter)


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


class Manager:
    """
    Summary of Manager operations
    """
    @staticmethod
    def get_by_config(conn, xml_config):
        """
        Initialize Manager
        :param conn: Database connection
        :param xml_config: XML profile information
        """
        return Manage(conn, xml_config)

    @staticmethod
    def get_by_string(conn, xml_string):
        """
        Get manager using string
        :param conn: Database connection
        :param xml_string: xml Character string
        :return: Manager
        """
        config = parse_config_from_string(xml_string)
        return Manage(conn, config)

    @staticmethod
    def get_by_file(conn, xml_path):
        """
        Get manager using XML file
        :param conn: Database connection
        :param xml_path: XML file path
        :return: Manager
        """
        config = parse_config_from_file(xml_path)
        return Manage(conn, config)


class Config:
    """
    Summary of Config operations
    """
    @staticmethod
    def parse_config_from_string(xml_string):
        """
        Parsing XML configuration string
        :param xml_string: XML configuration string
        :return: Profile information dictionary
        """
        return parse_config_from_string(xml_string)

    @staticmethod
    def parse_config_from_file(file_path):
        """
        Parsing XML configuration file
        :param file_path: Profile path
        :return: Profile information dictionary
        """
        return parse_config_from_file(file_path)


class MVC:
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


class MysqlMapper:
    """
    Summary of common operations
    """
    # Database connection holder
    Conn = Conn
    # SQL Execution Engine
    Engine = Engine
    # SQL template execution engine
    TemplateEngine = TemplateEngine
    # Build SQL string
    Builder = Builder
    # Database info
    Database = Database
    # Manager
    Manager = Manager
    # Config
    Config = Config
    # MVC
    MVC = MVC
