import collections
from typing import Tuple, List

from mysqlmapper.builder.sql import ConvertSQL

# database table
class SelectTable:

    # table name
    _name = None
    # this table sql
    _sql = None
    # need to query columns
    _columns = None

    def __init__(self, name: str):
        self._name = name
        self._sql = name
        self._columns = ["*"]

    def make_temp_table(self, cv_sql: ConvertSQL):
        """
        Set to temporary table
        :param cv_sql: Classes that implement the ConvertSQL interface
        """
        self._sql = "( %s ) AS %s" % (cv_sql.to_sql(), self._name)

    def set_columns(self, columns: Tuple[str] or List[str]):
        self._columns = columns

    def get_columns(self) -> str:
        _columns = []
        for column in self._columns:
            _columns.append("%s.`%s`" % (self._name, column))
        return ", ".join(_columns)

    def get_sql(self):
        return self._sql


# sql builder
class SQLBuilder(ConvertSQL):

    # table info
    _table = None

    _on = None
    _where = None

    _order_by = None
    _group_by = None

    _limit = None

    def __init__(self, table: SelectTable):
        self._table = table
        self._on = []
        self._where = []
        self._order_by = ""
        self._group_by = ""
        self._limit = (-1, 10)

    def on(self, sql: str):
        self._on.append(sql)
        return self

    def if_on(self, b: bool, sql: str):
        if b:
            self.on(sql)
        return self

    def where(self, sql: str):
        self._where.append(sql)
        return self

    def if_where(self, b: bool, sql: str):
        if b:
            self.where(sql)
        return self

    def order_by(self, order: str):
        self._order_by = order
        return self

    def group_by(self, group_by: str):
        self._group_by = group_by
        return self

    def limit(self, start: int, length: int):
        self._limit = (start, length)

    def to_sql(self) -> str:
        pass
