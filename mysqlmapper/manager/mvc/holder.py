from mysqlmapper.client import ConnHolder
from mysqlmapper.manager.info import get_db_info
from mysqlmapper.manager.mvc.dao import DAO
from mysqlmapper.manager.mvc.mapper import get_mapper_xml
from mysqlmapper.manager.mvc.service import Service
from mysqlmapper.manager.xml_config import parse_config_from_string


class MVCHolder:
    """
    MVC retainer
    """

    # Database connection
    conn_holder = None
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
        self.conn_holder = ConnHolder(host, user, password, database, charset)
        self.database_info = get_db_info(self.conn_holder.get_conn(), database)
        self.services = {}
        for table in self.database_info["tables"]:
            # get mapper xml
            xml_string = get_mapper_xml(self.database_info, table["Name"])
            # parse to config
            config = parse_config_from_string(xml_string)
            # get dao
            dao = DAO(self.conn_holder.get_conn(), config)
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
