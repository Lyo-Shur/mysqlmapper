from mysqlmapper.manager.manager import Manager


class DAO:
    """
    Dao layer
    """

    # Database manager
    _manager = None

    # Statement constants
    _get_list = "GetList"
    _get_count = "GetCount"
    _get_model = "GetModel"
    _update = "Update"
    _insert = "Insert"
    _delete = "Delete"

    def __init__(self, conn, config):
        """
        Initialize Dao layer
        :param conn: Database connection
        :param config: xml config
        """
        self._manager = Manager(conn, config)

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._manager.set_logger(logger)
        return self

    def get_list(self, parameter):
        """
        Get data list
        :param parameter: Search parameters
        :return: Data list
        """
        return self._manager.query(self._get_list, parameter)

    def get_count(self, parameter):
        """
        Quantity acquisition
        :param parameter: Search parameters
        :return: Number
        """
        return self._manager.count(self._get_count, parameter)

    def get_model(self, parameter):
        """
        Get record entity
        :param parameter: Search parameters
        :return: Record entity
        """
        list_dict = self._manager.query(self._get_model, parameter)
        if len(list_dict) == 0:
            return None
        return list_dict[0]

    def update(self, parameter):
        """
        Update record
        :param parameter: Update data
        :return: Update results
        """
        _, number = self._manager.exec(self._update, parameter)
        return number

    def insert(self, parameter):
        """
        insert record
        :param parameter: insert data
        :return: Insert results
        """
        number, _ = self._manager.exec(self._insert, parameter)
        return number

    def delete(self, parameter):
        """
        Delete data
        :param parameter: Delete data
        :return: Delete result
        """
        _, number = self._manager.exec(self._delete, parameter)
        return number
