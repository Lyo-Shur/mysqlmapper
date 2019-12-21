import pymysql


class ConnHolder:
    """
    数据库连接持有者
    """

    # 数据库连接
    _conn = None

    def __init__(self, host, user, password, database, charset="utf8"):
        """
        初始化数据库连接
        :param host: 主机名
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        :param charset: 编码格式
        :return:
        """
        self._conn = pymysql.connect(
            host=host,
            user=user, password=password,
            database=database,
            charset=charset)

    def get_conn(self):
        """
        获取数据库连接
        :return: 数据库连接
        """
        return self._conn
