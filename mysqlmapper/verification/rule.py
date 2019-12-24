import datetime
import re


class Rule:
    """
    Validation rule abstract class
    """

    def know(self, expr):
        """
        Identification verification rules
        :param expr: Rule expression
        :return: Boer
        """
        pass

    def check(self, dic, expr, name, value):
        """
        Verify expression and corresponding value
        :param dic: Original dictionary
        :param expr: Rule expression
        :param name: Parameter name
        :param value: Value to be verified
        :return: Verification results
        """
        pass


# Non empty calibration
class Required(Rule):
    def know(self, expr):
        return "required" == expr

    def check(self, dic, expr, name, value):
        b = isinstance(value, str)
        if not b:
            return b, name + " error in type"
        b = (value != "")
        if not b:
            return b, name + " Field cannot be empty"
        return b, "success"


# String length verification
class Length(Rule):
    expr = "length"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        b = isinstance(value, str)
        if not b:
            return b, name + " error in type"
        l = len(value)
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split("-")
        min = int(minmax[0])
        max = int(minmax[1])
        if l < min or l > max:
            return False, name + " Illegal field length"
        return True, "success"


# Digital range verification
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
            return False, name + " error in type"
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split("-")
        min = int(minmax[0])
        max = int(minmax[1])
        if value < min or value > max:
            return False, name + " Illegal field range"
        return True, "success"


# Time check
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
            return False, name + " error in type"
        return True, "success"


# Regular match check
class Regexp(Rule):
    expr = "regexp"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        search = re.search(pattern, value)
        if search is None:
            return False, name + " Illegal field format"
        start_end = search.span()
        if (start_end[1] - start_end[0]) != len(value):
            return False, name + " Illegal field format"
        return True, "success"
