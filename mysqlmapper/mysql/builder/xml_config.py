from xml.dom.minidom import parse, parseString


def parse_config_from_string(xml_string):
    """
    解析XML配置字符串
    :param xml_string: XML配置字符串
    :return: 配置文件信息字典
    """
    return _parse_config_from_doc(parseString(xml_string))


def parse_config_from_file(file_path):
    """
    解析XML配置文件
    :param file_path: 配置文件路径
    :return: 配置文件信息字典
    """
    return _parse_config_from_doc(parse(file_path))


def _parse_config_from_doc(doc):
    """
    解析doc文档
    :param doc: doc文档
    :return: 配置文件信息字典
    """
    # 预创建返回字典
    return_dict = {}
    root = doc.documentElement
    # 解析映射关系
    return_dict["mappers"] = {}
    for mapper in root.getElementsByTagName('mapper'):
        column = mapper.getAttribute("column")
        parameter = mapper.getAttribute("parameter")
        return_dict["mappers"][column] = parameter
    # 解析SQL语句
    return_dict["sqls"] = {}
    for sql in root.getElementsByTagName('sql'):
        key = sql.getElementsByTagName('key')[0].childNodes[0].data
        value = sql.getElementsByTagName('value')[0].childNodes[0].data
        return_dict["sqls"][key] = value
    return return_dict
