from typing import Dict

from tabledbmapper.engine import QueryResult, CountResult
from tabledbmapper.logger import Logger

from mysqlmapper.manager.mvc.dao import DAO


class Service:
    """
    Basic service layer
    """
    _dao = None

    def __init__(self, dao: DAO):
        """
        Initialize service layer
        :param dao: Dao layer
        """
        self._dao = dao

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._dao.set_logger(logger)
        return self

    def get_list(self, parameter: Dict, **kwargs) -> QueryResult:
        """
        Get data list
        :param parameter: Search parameters
        :return: Data list
        """
        return self._dao.get_list(parameter, **kwargs)

    def get_first(self, parameter: Dict, **kwargs) -> dict:
        """
        Get data list, then go back to the first record
        :param parameter: Search parameters
        :return: First Data
        """
        data_list = self.get_list(parameter, **kwargs)
        if len(data_list) == 0:
            return {}
        return data_list[0]

    def get_count(self, parameter: Dict) -> CountResult:
        """
        Quantity acquisition
        :param parameter: Search parameters
        :return: Number
        """
        return self._dao.get_count(parameter)

    def exist(self, parameter: Dict) -> bool:
        """
        Quantity acquisition, judge whether the quantity is greater than 0
        :param parameter: Search parameters
        :return: Number
        """
        return self._dao.exist(parameter)

    def get_model(self, parameter: Dict) -> Dict:
        """
        Get record entity
        :param parameter: Search parameters
        :return: Record entity
        """
        return self._dao.get_model(parameter)

    def insert(self, parameter: Dict) -> int:
        """
        insert record
        :param parameter: insert data
        :return: Insert results
        """
        return self._dao.insert(parameter)

    def update(self, parameter: Dict) -> int:
        """
        Update record
        :param parameter: Update data
        :return: Update results
        """
        return self._dao.update(parameter)

    def delete(self, parameter: Dict) -> int:
        """
        Delete data
        :param parameter: Delete data
        :return: Delete result
        """
        return self._dao.delete(parameter)
