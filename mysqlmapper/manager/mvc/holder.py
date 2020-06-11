from tabledbmapper.engine import TemplateEngine
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.mvc.dao import DAO
from tabledbmapper.manager.mvc.service import Service
from tabledbmapper.manager.xml_config import parse_config_from_string

from mysqlmapper.engine import MysqlEngine
from mysqlmapper.manager.info import get_db_info
from mysqlmapper.manager.mvc.mapper import get_mapper_xml


class MVCHolder:
    """
    MVC retainer
    """

    # Database connection
    template_engine = None
    # Database description information
    database_info = None
    # Service dictionary
    services = None

    def __init__(self, host, user, password, database, charset="utf8"):
        """
        Initialize MVC holder
        :param host: host name
        :param user: User name
        :param password: Password
        :param database: Database name
        :param charset: Encoding format
        """
        engine = MysqlEngine(host, user, password, database, charset)
        self.template_engine = TemplateEngine(engine)
        self.database_info = get_db_info(self.template_engine, database)
        self.services = {}
        for table in self.database_info["tables"]:
            # get mapper xml
            xml_string = get_mapper_xml(self.database_info, table["Name"])
            # parse to config
            config = parse_config_from_string(xml_string)
            # get manager
            manager = Manager(self.template_engine, config)
            # get dao
            dao = DAO(manager)
            # get service
            self.services[table["Name"]] = Service(dao)

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        for name in self.services:
            self.services[name].set_logger(logger)
        return self
