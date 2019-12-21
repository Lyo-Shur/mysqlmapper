from mysqlmapper.mysql.mvc.dao import DAO


class Service:
    """
    基础的Service层
    """
    _dao = None

    def __init__(self, conn, database_info, table_name):
        """
        初始化Service层
        :param conn: 数据库连接
        :param database_info: 数据库信息
        :param table_name: 表名
        """
        self._dao = DAO(conn, database_info, table_name)

    def get_list(self, parameter):
        """
        获取数据列表
        :param parameter: 搜索参数
        :return: 数据列表
        """
        return self._dao.get_list(parameter)

    def get_count(self, parameter):
        """
        获取数量
        :param parameter: 搜索参数
        :return: 数量
        """
        return self._dao.get_count(parameter)

    def get_model(self, parameter):
        """
        获取记录实体
        :param parameter: 搜索参数
        :return: 记录实体
        """
        return self._dao.get_model(parameter)

    def update(self, parameter):
        """
        更新记录
        :param parameter: 更新数据
        :return: 更新结果
        """
        return self._dao.update(parameter)

    def insert(self, parameter):
        """
        插入记录
        :param parameter: 插入数据
        :return: 插入结果
        """
        return self._dao.insert(parameter)

    def delete(self, parameter):
        """
        删除数据
        :param parameter: 删除数据
        :return: 删除结果
        """
        return self._dao.delete(parameter)
