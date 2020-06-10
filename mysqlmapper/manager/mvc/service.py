

class Service:
    """
    Basic service layer
    """
    _dao = None

    def __init__(self, dao):
        """
        Initialize service layer
        :param dao: Dao layer
        """
        self._dao = dao

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._dao.set_logger(logger)
        return self

    def get_list(self, parameter):
        """
        Get data list
        :param parameter: Search parameters
        :return: Data list
        """
        return self._dao.get_list(parameter)

    def get_count(self, parameter):
        """
        Quantity acquisition
        :param parameter: Search parameters
        :return: Number
        """
        return self._dao.get_count(parameter)

    def get_model(self, parameter):
        """
        Get record entity
        :param parameter: Search parameters
        :return: Record entity
        """
        return self._dao.get_model(parameter)

    def update(self, parameter):
        """
        Update record
        :param parameter: Update data
        :return: Update results
        """
        return self._dao.update(parameter)

    def insert(self, parameter):
        """
        insert record
        :param parameter: insert data
        :return: Insert results
        """
        return self._dao.insert(parameter)

    def delete(self, parameter):
        """
        Delete data
        :param parameter: Delete data
        :return: Delete result
        """
        return self._dao.delete(parameter)
