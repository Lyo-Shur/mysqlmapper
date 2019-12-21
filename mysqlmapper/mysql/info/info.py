from mysqlmapper.mysql.builder.xml_config import parse_config_from_string
from mysqlmapper.mysql.info.xml_info import index_xml, table_xml, column_xml, key_xml
from mysqlmapper.mysql.manager import Manager


def get_db_info(conn, database_name):
    """
    获取数据库信息
    :param conn: 数据库连接
    :param database_name: 数据库名
    :return: 数据库信息
    """
    # 读取配置文件
    table_config = parse_config_from_string(table_xml)
    column_config = parse_config_from_string(column_xml)
    index_config = parse_config_from_string(index_xml)
    key_config = parse_config_from_string(key_xml)

    # 查询表结构信息
    tables = Manager(conn, table_config).query("GetList", {"data_base_name": database_name})
    for table in tables:
        table["columns"] = Manager(conn, column_config) \
            .query("GetList", {"data_base_name": database_name, "table_name": table["Name"]})
        table["indexs"] = Manager(conn, index_config) \
            .query("GetList", {"data_base_name": database_name, "table_name": table["Name"]})
        table["keys"] = Manager(conn, key_config) \
            .query("GetList", {"data_base_name": database_name, "table_name": table["Name"]})
    return {"Name": database_name, "tables": tables}
