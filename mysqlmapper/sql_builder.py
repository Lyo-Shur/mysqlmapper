from jinja2 import Template
import re


def builder(template, parameter):
    """
    Build SQL string
    :param template: Init jinja2 template
    :param parameter: Parameter
    :return: Jinja2 template return
    """
    # Build template
    template = Template(_parsing(template))
    # Render parameter
    template = template.render(parameter)
    # Extract_parameters
    result, parameters = _extract_parameters(template)
    # Clean string
    result = _trim(result)
    # Execution patch
    result = _deal_with_update(result)
    parameters = _deal_with_limit(result, parameters)
    # Return rendering results
    return result, parameters


def _parsing(template):
    """
    Extend the native jinja2 syntax to support parameterized queries
    :param template: Original string
    :return: Converted results
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
    Parameter extraction
    :param template: Template of parameters to be extracted
    :return: Extraction results
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
    Cleaning SQL statements
    :param template: SQL statement to be cleaned
    :return: Cleaning result
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
    For the patch of UPDATE statement, avoid redundant commas in update set
    :param template: Template
    :return: Results after treatment
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
    Handle limit patch
    :param template: Template
    :return: Results after treatment
    """
    up_template = template.upper()
    index = up_template.find("LIMIT")
    if index == -1:
        return parameters
    count = template[:index].count("%s")
    parameters[count] = int(parameters[count])
    parameters[count + 1] = int(parameters[count + 1])
    return parameters
