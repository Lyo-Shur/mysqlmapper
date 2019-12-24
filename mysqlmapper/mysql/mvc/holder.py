from mysqlmapper.mysql.client import ConnHolder
from mysqlmapper.mysql.info.info import get_db_info
from mysqlmapper.mysql.mvc.service import Service


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
            self.services[table["Name"]] = Service(self.conn_holder.get_conn(), self.database_info, table["Name"])
