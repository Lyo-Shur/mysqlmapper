from mysqlmapper.mysql.client import ConnHolder
from mysqlmapper.mysql.info.info import get_db_info
from mysqlmapper.mysql.mvc.service import Service


class MVCHolder:
    """
    MVC保持器
    """

    # 数据库连接
    conn_holder = None
    # 数据库描述信息
    database_info = None
    # service字典
    services = None

    def __init__(self, host, user, password, database, charset="utf8"):
        """
        初始化MVC保持器
        :param host: 主机名
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        :param charset: 编码格式
        """
        self.conn_holder = ConnHolder(host, user, password, database, charset)
        self.database_info = get_db_info(self.conn_holder.get_conn(), database)
        self.services = {}
        for table in self.database_info["tables"]:
            self.services[table["Name"]] = Service(self.conn_holder.get_conn(), self.database_info, table["Name"])
