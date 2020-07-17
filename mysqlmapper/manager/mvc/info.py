from typing import Dict

from tabledbmapper.engine import TemplateEngine
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.xml_config import parse_config_from_string

_table_xml = """
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

_column_xml = """
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

_index_xml = """
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

_key_xml = """
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

DataBaseInfo = Dict


def get_db_info(template_engine: TemplateEngine, database_name: str) -> DataBaseInfo:
    """
    Get database information
    :param template_engine: SQL template execution engine
    :param database_name: Database name
    :return: database information
    """
    # Read profile
    table_config = parse_config_from_string(_table_xml)
    column_config = parse_config_from_string(_column_xml)
    index_config = parse_config_from_string(_index_xml)
    key_config = parse_config_from_string(_key_xml)

    # builder manager
    table_manager = Manager(template_engine, table_config)
    column_manager = Manager(template_engine, column_config)
    index_manager = Manager(template_engine, index_config)
    key_manager = Manager(template_engine, key_config)

    # Query table structure information
    tables = table_manager.query("GetList", {"data_base_name": database_name})
    for table in tables:
        table["columns"] = column_manager.query(
            "GetList",
            {"data_base_name": database_name, "table_name": table["Name"]}
        )
        table["indexs"] = index_manager.query(
            "GetList",
            {"data_base_name": database_name, "table_name": table["Name"]}
        )
        table["keys"] = key_manager.query(
            "GetList",
            {"data_base_name": database_name, "table_name": table["Name"]}
        )
    return {"Name": database_name, "tables": tables}
