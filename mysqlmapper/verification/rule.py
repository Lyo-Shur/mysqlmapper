import datetime
import re


class Rule:
    """
    校验规则抽象类
    """

    def know(self, expr):
        """
        识别校验规则
        :param expr: 规则表达式
        :return: 布尔
        """
        pass

    def check(self, dic, expr, name, value):
        """
        校验表达式和对应值
        :param dic: 原始字典
        :param expr: 规则表达式
        :param name: 参数名
        :param value: 待校验的值
        :return: 验证结果
        """
        pass


# 非空校验
class Required(Rule):
    def know(self, expr):
        return "required" == expr

    def check(self, dic, expr, name, value):
        b = isinstance(value, str)
        if not b:
            return b, name + "类型错误"
        b = (value != "")
        if not b:
            return b, name + "字段不能为空"
        return b, "success"


# 字符串长度校验
class Length(Rule):
    expr = "length"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        b = isinstance(value, str)
        if not b:
            return b, name + "类型错误"
        l = len(value)
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split("-")
        min = int(minmax[0])
        max = int(minmax[1])
        if l < min or l > max:
            return False, name + "字段长度非法"
        return True, "success"


# 数字范围校验
class Range(Rule):
    expr = "range"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        try:
            value = int(value)
            dic[name] = value
        except Exception as e:
            print(e)
            return False, name + "类型错误"
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split("-")
        min = int(minmax[0])
        max = int(minmax[1])
        if value < min or value > max:
            return False, name + "字段范围非法"
        return True, "success"


# 时间校验
class DateTime(Rule):
    expr = "datetime"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        try:
            value = datetime.datetime.strptime(value, pattern)
            dic[name] = value
        except Exception as e:
            print(e)
            return False, name + "类型错误"
        return True, "success"


# 正则匹配校验
class Regexp(Rule):
    expr = "regexp"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        search = re.search(pattern, value)
        if search is None:
            return False, name + "字段格式非法"
        start_end = search.span()
        if (start_end[1] - start_end[0]) != len(value):
            return False, name + "字段格式非法"
        return True, "success"
