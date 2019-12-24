from xml.dom.minidom import parse, parseString


def parse_config_from_string(xml_string):
    """
    Parsing XML configuration string
    :param xml_string: XML configuration string
    :return: Profile information dictionary
    """
    return _parse_config_from_doc(parseString(xml_string))


def parse_config_from_file(file_path):
    """
    Parsing XML configuration file
    :param file_path: Profile path
    :return: Profile information dictionary
    """
    return _parse_config_from_doc(parse(file_path))


def _parse_config_from_doc(doc):
    """
    Parsing DOC documents
    :param doc: Doc document
    :return: Profile information dictionary
    """
    # Pre create return dictionary
    return_dict = {}
    root = doc.documentElement
    # Analytic mapping
    return_dict["mappers"] = {}
    for mapper in root.getElementsByTagName('mapper'):
        column = mapper.getAttribute("column")
        parameter = mapper.getAttribute("parameter")
        return_dict["mappers"][column] = parameter
    # Parsing SQL statements
    return_dict["sqls"] = {}
    for sql in root.getElementsByTagName('sql'):
        key = sql.getElementsByTagName('key')[0].childNodes[0].data
        value = sql.getElementsByTagName('value')[0].childNodes[0].data
        return_dict["sqls"][key] = value
    return return_dict
