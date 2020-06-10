from mysqlmapper.logger import Logger
from mysqlmapper.manager.xml_config import parse_config_from_string
from mysqlmapper.manager.manager import Manager


table_xml = """
<xml>
    <mapper column="TABLE_NAME" parameter="Name"/>
    <mapper column="ENGINE" parameter="Engine"/>
    <mapper column="TABLE_COLLATION" parameter="Collation"/>
    <mapper column="TABLE_COMMENT" parameter="Comment"/>
    <mapper column="IFNULL(AUTO_INCREMENT, -1)" parameter="AutoIncrement"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                TABLE_NAME, ENGINE, TABLE_COLLATION, TABLE_COMMENT, IFNULL(AUTO_INCREMENT, -1)
            FROM
                information_schema.TABLES
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_TYPE = 'BASE TABLE'
        </value>
    </sql>
</xml>
"""

column_xml = """
<xml>
    <mapper column="ORDINAL_POSITION" parameter="Number"/>
    <mapper column="COLUMN_NAME" parameter="Name"/>
    <mapper column="COLUMN_TYPE" parameter="Type"/>
    <mapper column="IS_NULLABLE" parameter="NullAble"/>
    <mapper column="COLUMN_DEFAULT" parameter="Defaule"/>
    <mapper column="COLUMN_COMMENT" parameter="Comment"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                ORDINAL_POSITION,
                COLUMN_NAME,
                COLUMN_TYPE,
                IS_NULLABLE,
                IFNULL(COLUMN_DEFAULT, ''),
                COLUMN_COMMENT
            FROM
                information_schema.COLUMNS
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""

index_xml = """
<xml>
    <mapper column="INDEX_NAME" parameter="Name"/>
    <mapper column="COLUMN_NAME" parameter="ColumnName"/>
    <mapper column="NON_UNIQUE" parameter="Unique"/>
    <mapper column="INDEX_TYPE" parameter="Type"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                INDEX_NAME,
                COLUMN_NAME,
                NON_UNIQUE,
                INDEX_TYPE
            FROM
                information_schema.STATISTICS
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""

key_xml = """
<xml>
    <mapper column="COLUMN_NAME" parameter="ColumnName"/>
    <mapper column="REFERENCED_TABLE_NAME" parameter="RelyTable"/>
    <mapper column="REFERENCED_COLUMN_NAME" parameter="RelyColumnName"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM
                information_schema.KEY_COLUMN_USAGE
            WHERE
                CONSTRAINT_NAME != 'PRIMARY' AND
                TABLE_SCHEMA = REFERENCED_TABLE_SCHEMA AND
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""


def get_db_info(conn, database_name, logger=Logger()):
    """
    Get database information
    :param conn: Database connection
    :param database_name: Database name
    :param logger: Logger
    :return: database information
    """
    # Read profile
    table_config = parse_config_from_string(table_xml)
    column_config = parse_config_from_string(column_xml)
    index_config = parse_config_from_string(index_xml)
    key_config = parse_config_from_string(key_xml)

    # Query table structure information
    tables = Manager(conn, table_config) \
        .set_logger(logger) \
        .query("GetList", {"data_base_name": database_name})
    for table in tables:
        table["columns"] = Manager(conn, column_config) \
            .set_logger(logger) \
            .query("GetList", {"data_base_name": database_name, "table_name": table["Name"]})
        table["indexs"] = Manager(conn, index_config) \
            .set_logger(logger) \
            .query("GetList", {"data_base_name": database_name, "table_name": table["Name"]})
        table["keys"] = Manager(conn, key_config) \
            .set_logger(logger) \
            .query("GetList", {"data_base_name": database_name, "table_name": table["Name"]})
    return {"Name": database_name, "tables": tables}
