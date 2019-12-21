from mysqlmapper.mysql.builder.sql_builder import sql_builder
from mysqlmapper.mysql.builder.xml_config import parse_config_from_string, parse_config_from_file
from mysqlmapper.mysql.engine import Engine
from mysqlmapper.mysql.generate.mapper import get_mapper_xml


class Manager:
    # 数据库连接
    conn = None
    # xml配置文件属性
    xml_config = None

    def __init__(self, conn, xml_config):
        """
        初始化Manager
        :param conn: 数据库连接
        :param xml_config: XML配置文件信息
        """
        self.conn = conn
        self.xml_config = xml_config

    def query(self, key, parameter):
        """
        查询结果集
        :param key: SQL别名
        :param parameter: 执行参数
        :return: 执行结果
        """
        # 获取SQL
        sql = self.xml_config["sqls"][key]
        # 渲染模板
        result, parameters = sql_builder(sql, parameter)
        print("当前执行的SQL>>>", result, parameters)
        # 执行SQL
        query_list = Engine.query(self.conn, result, parameters)
        # 翻译别名
        list = []
        for query_item in query_list:
            item = {}
            for t in query_item.items():
                if t[0] in self.xml_config["mappers"]:
                    item[self.xml_config["mappers"][t[0]]] = t[1]
                    continue
                item[t[0]] = t[1]
            list.append(item)
        return list

    def count(self, key, parameter):
        """
        查询数量
        :param key: SQL别名
        :param parameter: 执行参数
        :return: 执行结果
        """
        # 获取SQL
        sql = self.xml_config["sqls"][key]
        # 渲染模板
        result, parameters = sql_builder(sql, parameter)
        print("当前执行的SQL>>>", result, parameters)
        # 执行SQL
        return Engine.count(self.conn, result, parameters)

    def exec(self, key, parameter):
        """
        执行SQL
        :param key: SQL别名
        :param parameter: 执行参数
        :return: 执行结果
        """
        # 获取SQL
        sql = self.xml_config["sqls"][key]
        # 渲染模板
        result, parameters = sql_builder(sql, parameter)
        print("当前执行的SQL>>>", result, parameters)
        # 执行SQL
        return Engine.exec(self.conn, result, parameters)


def get_manager_by_string(conn, xml_string):
    """
    使用字符串获取Manager
    :param conn: 数据库连接
    :param xml_string: xml字符串
    :return: Manager
    """
    # 获取config
    config = parse_config_from_string(xml_string)
    return Manager(conn, config)


def get_manager_by_file(conn, xml_path):
    """
    使用XML文件获取Manager
    :param conn: 数据库连接
    :param xml_path: xml文件路径
    :return: Manager
    """
    # 获取config
    config = parse_config_from_file(xml_path)
    return Manager(conn, config)


def get_manager_by_dbinfo(conn, database_info, table_name):
    """
    使用数据库信息获取Manager
    :param conn: 数据库连接
    :param database_info: 数据库信息
    :param table_name: 表名
    :return: Manager
    """
    # 获取xml
    xml_string = get_mapper_xml(database_info, table_name)
    return get_manager_by_string(conn, xml_string)
