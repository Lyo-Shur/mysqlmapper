from jinja2 import Template
import re


def sql_builder(template, parameter):
    """
    组建SQL语句
    :param template: 初始jinja2模板
    :param parameter: 渲染参数
    :return: 渲染结果
    """
    # 组建模板
    template = Template(_parsing(template))
    # 渲染模板
    template = template.render(parameter)
    # 提取参数
    result, parameters = _extract_parameters(template)
    # 执行清洗
    result = _trim(result)
    # 执行补丁
    result = _deal_with_update(result)
    parameters = _deal_with_limit(result, parameters)
    # 返回渲染结果
    return result, parameters


def _parsing(template):
    """
    拓展原生jinja2语法，便于支持参数化查询
    :param template: 原始字符串
    :return: 转换后的结果
    """
    result = template
    rule = r'(#{)(.*?)(})'
    search = re.search(rule, result)
    while search:
        result = result.replace(search.group(0), "<![Parameter[{{" + search.group(2) + "}}]]>")
        search = re.search(rule, result)
    return result


def _extract_parameters(template):
    """
    参数提取
    :param template: 待提取参数的模板
    :return: 提取结果
    """
    result = template
    parameters = []
    rule = r'(<!\[Parameter\[)((.|\s|\S)*?)(\]\]>)'
    search = re.search(rule, result)
    while search:
        result = result[:search.span()[0]] + "%s" + result[search.span()[1]:]
        parameter = search.group(2)
        parameters.append(parameter)
        search = re.search(rule, result)
    return result, parameters


def _trim(template):
    """
    对SQL语句执行清洗
    :param template: 待清洗的SQL语句
    :return: 清洗结果
    """
    template = template.strip()
    template = template.replace("\n", " ")
    template = template.replace("\t", " ")
    template = template.replace("\r", " ")
    number = 0
    while number != len(template):
        number = len(template)
        template = template.replace("  ", " ")
    return template


def _deal_with_update(template):
    """
    针对更新语句的补丁，避免更新set出现多余的逗号
    :param template: 模板
    :return: 处理后的结果
    """
    up_template = template.upper()
    index_update = up_template.find("UPDATE")
    index_where = up_template.find("WHERE")
    if index_update != -1 and index_where != -1:
        index_where -= 1
        while index_where > 0:
            char = up_template[index_where]
            if char == ' ':
                index_where -= 1
                continue
            if char == ',':
                template = template[:index_where] + template[index_where + 1:]
            break
    return template


def _deal_with_limit(template, parameters):
    """
    处理limit补丁
    :param template: 模板
    :return: 处理后的结果
    """
    up_template = template.upper()
    index = up_template.find("LIMIT")
    if index == -1:
        return parameters
    count = template[:index].count("%s")
    parameters[count] = int(parameters[count])
    parameters[count + 1] = int(parameters[count + 1])
    return parameters
