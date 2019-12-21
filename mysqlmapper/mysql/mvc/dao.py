from mysqlmapper.mysql.manager import get_manager_by_dbinfo


class DAO:
    # 数据库Manager
    _manager = None

    # 语句常量
    _get_list = "GetList"
    _get_count = "GetCount"
    _get_model = "GetModel"
    _update = "Update"
    _insert = "Insert"
    _delete = "Delete"

    def __init__(self, conn, database_info, table_name):
        """
        初始化dao层
        :param conn: 数据库连接
        :param database_info: 数据库信息
        :param table_name: 表名
        """
        self._manager = get_manager_by_dbinfo(conn, database_info, table_name)

    def get_list(self, parameter):
        """
        获取数据列表
        :param parameter: 搜索参数
        :return: 数据列表
        """
        return self._manager.query(self._get_list, parameter)

    def get_count(self, parameter):
        """
        获取数量
        :param parameter: 搜索参数
        :return: 数量
        """
        return self._manager.count(self._get_count, parameter)

    def get_model(self, parameter):
        """
        获取记录实体
        :param parameter: 搜索参数
        :return: 记录实体
        """
        list_dict = self._manager.query(self._get_model, parameter)
        if len(list_dict) == 0:
            return None
        return list_dict[0]

    def update(self, parameter):
        """
        更新记录
        :param parameter: 更新数据
        :return: 更新结果
        """
        _, number = self._manager.exec(self._update, parameter)
        return number

    def insert(self, parameter):
        """
        插入记录
        :param parameter: 插入数据
        :return: 插入结果
        """
        id, _ = self._manager.exec(self._insert, parameter)
        return id

    def delete(self, parameter):
        """
        删除数据
        :param parameter: 删除数据
        :return: 删除结果
        """
        _, number = self._manager.exec(self._delete, parameter)
        return number
