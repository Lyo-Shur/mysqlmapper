from mysqlmapper.verification.rule import *


class Helper:
    """
    格式校验帮助类
    """

    # 参数字典
    _dict_parameter = None
    # 校验配置
    _configs = None
    # 内置校验规则
    _rules = []

    def __init__(self, dict_parameter, configs):
        """
        初始化校验帮助工具类
        :param dict_parameter: 参数字典
        :param configs: 规则字典
        """
        self._dict_parameter = dict_parameter
        self._configs = configs
        self._rules.append(Required())
        self._rules.append(Length())
        self._rules.append(Range())
        self._rules.append(DateTime())
        self._rules.append(Regexp())

    def weak_check(self):
        """
        弱校验，当参数不存在时，略过
        :return: 校验结果
        """
        for config in self._configs.items():
            name = config[0]
            expr = config[1]
            if name not in self._dict_parameter:
                continue
            # 规则匹配标志位
            flag = False
            for rule in self._rules:
                if rule.know(expr):
                    flag = True
                    b, message = rule.check(self._dict_parameter, expr, name, self._dict_parameter[name])
                    if not b:
                        return b, message
            if not flag:
                return False, "校验规则不存在"
        return True, "success"

    def check(self):
        """
        强校验，当参数不存在时，返回校验错误
        :return: 校验结果
        """
        for config in self._configs.items():
            name = config[0]
            expr = config[1]
            if name not in self._dict_parameter:
                return False, name + "参数不存在"
            # 规则匹配标志位
            flag = False
            for rule in self._rules:
                if rule.know(expr):
                    flag = True
                    b, message = rule.check(self._dict_parameter, expr, name, self._dict_parameter[name])
                    if not b:
                        return b, message
                    break

            if not flag:
                return False, "校验规则不存在"
        return True, "success"
