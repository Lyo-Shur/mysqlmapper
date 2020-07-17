from tabledbmapper.logger import DefaultLogger
from tabledbmapper.manager.mvc.service import Service
from tabledbmapper.manager.session.sql_session_factory import SQLSessionFactory, SQLSessionFactoryBuild

from mysqlmapper.engine import MySQLConnHandle, MySQLExecuteEngine, MySQLConnBuilder
from mysqlmapper.manager.mvc.holder import MVCHolder


class MySQLSessionFactory(SQLSessionFactory):

    # mvc holder
    _mvc_holder = None

    def __init__(self, conn_builder: MySQLConnBuilder, conn_handle: MySQLConnHandle, execute_engine: MySQLExecuteEngine,
                 lazy_init=True, max_conn_number=10, enable_simple_service=True, logger=DefaultLogger()):
        """
        Init session pool
        :param conn_builder: MySQLConnBuilder
        :param conn_handle: MySQLConnHandle
        :param execute_engine: MySQLExecuteEngine
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        :param enable_simple_service: enable  simple service
        :param logger: Logger
        """
        self._mvc_holder = MVCHolder(
            conn_builder.host,
            conn_builder.user,
            conn_builder.password,
            conn_builder.database,
            enable_simple_service,
            conn_builder.charset
        )
        self._mvc_holder.set_logger(logger)
        super().__init__(conn_builder, conn_handle, execute_engine, lazy_init, max_conn_number, logger)

    def get_common_session(self):
        return self._mvc_holder.session

    def get_simple_service(self, table_name: str) -> Service:
        return self._mvc_holder.services[table_name]

    def get_database_info(self):
        return self._mvc_holder.database_info


class MySQLSessionFactoryBuild(SQLSessionFactoryBuild):

    _enable_simple_service = True

    def __init__(self, host: str, user: str, password: str, database: str, charset="utf8"):
        """
        Init
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        conn_builder = MySQLConnBuilder(host, user, password, database, charset)
        super().__init__(conn_builder, MySQLConnHandle(), MySQLExecuteEngine())

    def close_simple_service(self):
        self._enable_simple_service = False
        return self

    # 这没写完
    def build(self) -> MySQLSessionFactory:
        return MySQLSessionFactory(
            self._conn_builder,
            self._conn_handle,
            self._execute_engine,
            self._lazy_init,
            self._max_conn_number,
            self._enable_simple_service
        )
