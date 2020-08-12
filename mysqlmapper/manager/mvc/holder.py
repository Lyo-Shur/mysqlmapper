from tabledbmapper.logger import DefaultLogger, Logger
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.session.sql_session import SQLSession
from tabledbmapper.manager.xml_config import parse_config_from_string

from mysqlmapper.engine import MySQLConnBuilder, MySQLTemplateEngine
from mysqlmapper.manager.mvc.dao import DAO
from mysqlmapper.manager.mvc.info import get_db_info
from mysqlmapper.manager.mvc.mapper import get_mapper_xml
from mysqlmapper.manager.mvc.service import Service


class MVCHolder:
    """
    MVC retainer
    """

    # Database session
    session = None
    # Database description information
    database_info = None
    # Service dictionary
    services = None

    def __init__(self, host: str, user: str, password: str, database: str, enable_simple_service=True, charset="utf8"):
        """
        Initialize MVC holder
        :param host: host name
        :param user: User name
        :param password: Password
        :param database: Database name
        :param charset: Encoding format
        """
        conn_handle = MySQLConnBuilder(host, user, password, database, charset)
        conn = conn_handle.connect()
        template_engine = MySQLTemplateEngine(conn)

        self.session = SQLSession(template_engine)

        if enable_simple_service:
            self.session.engine().set_logger(Logger())
            self.database_info = get_db_info(self.session.engine(), database)
            self.services = {}
            for table in self.database_info["tables"]:
                # get mapper xml
                xml_string = get_mapper_xml(self.database_info, table["Name"])
                # parse to config
                config = parse_config_from_string(xml_string)
                # get manager
                manager = Manager(self.session.engine(), config)
                # get dao
                dao = DAO(manager)
                # get service
                self.services[table["Name"]] = Service(dao)
            self.session.engine().set_logger(DefaultLogger())

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self.session.engine().set_logger(logger)
        return self
