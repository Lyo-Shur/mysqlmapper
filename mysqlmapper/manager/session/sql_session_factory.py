from tabledbmapper.logger import DefaultLogger
from tabledbmapper.manager.session.sql_session_factory import SQLSessionFactory, SQLSessionFactoryBuild

from mysqlmapper.engine import MysqlConnHandle, MysqlExecuteEngine
from mysqlmapper.manager.mvc.holder import MVCHolder


class MySQLSessionFactory(SQLSessionFactory):

    # mvc holder
    MVCHolder = None

    def __init__(self, conn_handle: MysqlConnHandle, execute_engine: MysqlExecuteEngine,
                 lazy_init=True, max_conn_number=10, enable_mvcholder=True, logger=DefaultLogger()):
        """
        Init session pool
        :param conn_handle: ConnHandle
        :param execute_engine: ExecuteEngine
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        :param enable_mvcholder: enable mvc holder
        :param logger: Logger
        """
        if enable_mvcholder:
            self.MVCHolder = MVCHolder(
                conn_handle.host,
                conn_handle.user,
                conn_handle.password,
                conn_handle.database,
                conn_handle.charset
            )
        super().__init__(conn_handle, execute_engine, lazy_init, max_conn_number, logger)


class MySQLSessionFactoryBuild(SQLSessionFactoryBuild):

    _conn_handle = None
    _execute_engine = None

    _lazy_init = True
    _max_conn_number = 10

    _enable_mvc_holder = True

    def __init__(self, host: str, user: str, password: str, database: str, charset="utf8"):
        """
        Init
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        conn_handle = MysqlConnHandle(host, user, password, database, charset)
        execute_engine = MysqlExecuteEngine()
        super().__init__(conn_handle, execute_engine)

    def close_mvc_holder(self):
        self._enable_mvc_holder = False
        return self

    def build(self) -> MySQLSessionFactory:
        return MySQLSessionFactory(
            self._conn_handle,
            self._execute_engine,
            self._lazy_init,
            self._max_conn_number,
            self._enable_mvc_holder
        )
