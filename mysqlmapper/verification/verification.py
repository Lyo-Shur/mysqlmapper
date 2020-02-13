from mysqlmapper.verification.rule import *


class Helper:
    """
    Format verification help class
    """

    # Parameter dictionary
    _dict_parameter = None
    # Check configuration
    _configs = None
    # Built in verification rules
    _rules = []

    def __init__(self, dict_parameter, configs):
        """
        Initialize verification help tool class
        :param dict_parameter: Parameter dictionary
        :param configs: Rule dictionary
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
        Weak check, skip when parameter does not exist
        :return: Verification result
        """
        for config in self._configs.items():
            name = config[0]
            expr = config[1]
            if name not in self._dict_parameter:
                continue
            # Rule matching flag bit
            flag = False
            for rule in self._rules:
                if rule.know(expr):
                    flag = True
                    b, message = rule.check(self._dict_parameter, expr, name, self._dict_parameter[name])
                    if not b:
                        return b, message
                    break
            if not flag:
                return False, "Validation rule does not exist"
        return True, "success"

    def check(self):
        """
        Strong check. When the parameter does not exist, a check error is returned
        :return: Verification result
        """
        for config in self._configs.items():
            name = config[0]
            expr = config[1]
            if name not in self._dict_parameter:
                return False, name + " Parameter does not exist"
            # Rule matching flag bit
            flag = False
            for rule in self._rules:
                if rule.know(expr):
                    flag = True
                    b, message = rule.check(self._dict_parameter, expr, name, self._dict_parameter[name])
                    if not b:
                        return b, message
                    break

            if not flag:
                return False, "Validation rule does not exist"
        return True, "success"
