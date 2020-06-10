from mysqlmapper.engine import TemplateEngine


class Manager:
    # SQL template execution engine
    _template_engine = None
    # XML profile properties
    xml_config = None

    def __init__(self, conn, xml_config):
        """
        Initialize Manager
        :param conn: Database connection
        :param xml_config: XML profile information
        """
        self._template_engine = TemplateEngine(conn)
        self.xml_config = xml_config

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._template_engine.set_logger(logger)
        return self

    def query(self, key, parameter):
        """
        Query result set
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        # Get SQL
        sql_template = self.xml_config["sqls"][key]
        # Implementation of SQL
        query_list = self._template_engine.query(sql_template, parameter)
        # Translation alias
        data = []
        for query_item in query_list:
            item = {}
            for t in query_item.items():
                if t[0] in self.xml_config["mappers"]:
                    item[self.xml_config["mappers"][t[0]]] = t[1]
                    continue
                item[t[0]] = t[1]
            data.append(item)
        return data

    def count(self, key, parameter):
        """
        Query quantity
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        # Get SQL
        sql_template = self.xml_config["sqls"][key]
        # Implementation of SQL
        return self._template_engine.count(sql_template, parameter)

    def exec(self, key, parameter):
        """
        Implementation of SQL
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        # Get SQL
        sql_template = self.xml_config["sqls"][key]
        # Implementation of SQL
        return self._template_engine.exec(sql_template, parameter)
