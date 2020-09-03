from jinja2 import Environment

from mysqlmapper.manager.mvc.info import DataBaseInfo

# noinspection SpellCheckingInspection
_mapper_xml = """
<xml>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                {% for column in table.columns %}`{{ column.Name }}`{% if not loop.last %}, {% endif %}{% endfor %}
            FROM
                `{{table.Name}}`
            WHERE
    {% for column in table.columns %}
        {% if column.Name != key %}
            {% if column.Type|clear_type in int_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} } AND
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in float_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} } AND
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in date_types %}
                {% if column.Type|clear_type == "date" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "time" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%H:%M:%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "year" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "timestamp" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y%m%d%H%M%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "datetime" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
            {% endif %}
            {% if column.Type|clear_type in string_types %}
                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} 
                    `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND 
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
        {% endif %}
    {% endfor %}
            1 = 1
            {{ "{"|echo }}% if (mysql_mapper_order_by | default("")) != "" %{{ "}"|echo }} 
                ORDER BY {{ "{"|echo }}{ mysql_mapper_order_by }{{ "}"|echo }} 
            {{ "{"|echo }}% endif %{{ "}"|echo }} 
            {{ "{"|echo }}% if (mysql_mapper_limit_start | default(-1)) != -1 %{{ "}"|echo }} 
                LIMIT #{ mysql_mapper_limit_start }, #{ mysql_mapper_limit_length | default(10) } 
            {{ "{"|echo }}% endif %{{ "}"|echo }}
        </value>
    </sql>
    <sql>
        <key>GetCount</key>
        <value>
            SELECT
                COUNT(1)
            FROM
                `{{table.Name}}`
            WHERE
    {% for column in table.columns %}
        {% if column.Name != key %}
            {% if column.Type|clear_type in int_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} } AND
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in float_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} } AND
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in date_types %}
                {% if column.Type|clear_type == "date" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "time" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%H:%M:%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "year" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "timestamp" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y%m%d%H%M%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "datetime" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
            {% endif %}
            {% if column.Type|clear_type in string_types %}
                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} 
                    `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND 
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
        {% endif %}
    {% endfor %}
            1 = 1
        </value>
    </sql>
    <sql>
        <key>Exist</key>
        <value>
            SELECT
                COUNT(1)
            FROM
                `{{table.Name}}`
            WHERE
    {% for column in table.columns %}
        {% if column.Name != key %}
            {% if column.Type|clear_type in int_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} } AND
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in float_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} } AND
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in date_types %}
                {% if column.Type|clear_type == "date" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "time" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%H:%M:%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "year" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "timestamp" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y%m%d%H%M%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "datetime" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") } AND
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
            {% endif %}
            {% if column.Type|clear_type in string_types %}
                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} 
                    `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND 
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
        {% endif %}
    {% endfor %}
            1 = 1
            LIMIT 0, 1
        </value>
    </sql>
    <sql>
        <key>GetModel</key>
        <value>
            SELECT
                {% for column in table.columns %}`{{ column.Name }}`{% if not loop.last %}, {% endif %}{% endfor %}
            FROM
                `{{table.Name}}`
            WHERE
                `{{key}}` = #{ {{key}} }
        </value>
    </sql>
    <sql>
        <key>Insert</key>
        <value>
            INSERT INTO `{{table.Name}}`
            (
        {% for column in table.columns %}
            {% if column.Name != key or table.AutoIncrement == -1 %}
                `{{ column.Name }}`{% if not loop.last %}, {% endif %}
            {% endif %}
        {% endfor %}
            )
            VALUES
            (
    {% for column in table.columns %}
        {% if column.Name != key or table.AutoIncrement == -1 %}
            {% if column.Type|clear_type in int_types %}
                #{ {{column.Name}} }
            {% endif %}
            {% if column.Type|clear_type in float_types %}
                #{ {{column.Name}} }
            {% endif %}
            {% if column.Type|clear_type in date_types %}
                {% if column.Type|clear_type == "date" %}
                    #{ {{column.Name}}.strftime("%Y-%m-%d") }
                {% endif %}
                {% if column.Type|clear_type == "time" %}
                    #{ {{column.Name}}.strftime("%H:%M:%S") }
                {% endif %}
                {% if column.Type|clear_type == "year" %}
                    #{ {{column.Name}}.strftime("%Y") }
                {% endif %}
                {% if column.Type|clear_type == "timestamp" %}
                    #{ {{column.Name}}.strftime("%Y%m%d%H%M%S") }
                {% endif %}
                {% if column.Type|clear_type == "datetime" %}
                    #{ {{column.Name}}.strftime("%Y-%m-%d %H:%M:%S") }
                {% endif %}
            {% endif %}
            {% if column.Type|clear_type in string_types %}
                #{ {{column.Name}} }
            {% endif %}
            {% if not loop.last %}, {% endif %}
        {% endif %}
    {% endfor %}
            )
        </value>
    </sql>
    <sql>
        <key>Update</key>
        <value>
            UPDATE `{{table.Name}}` SET
    {% for column in table.columns %}
        {% if column.Name != key %}
            {% if column.Type|clear_type in int_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} },
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in float_types %}
                {{ "{"|echo }}% if {{ column.Name }} and {{ column.Name }} != 0 %{{ "}"|echo }}
                    `{{ column.Name }}` = #{ {{ column.Name }} },
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
            {% if column.Type|clear_type in date_types %}
                {% if column.Type|clear_type == "date" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d") },
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "time" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%H:%M:%S") },
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "year" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y") },
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "timestamp" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y%m%d%H%M%S") },
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
                {% if column.Type|clear_type == "datetime" %}
                    {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}
                        `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") },
                    {{ "{"|echo }}% endif %{{ "}"|echo }}
                {% endif %}
            {% endif %}
            {% if column.Type|clear_type in string_types %}
                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} 
                    `{{ column.Name }}` = #{ {{ column.Name }} },
                {{ "{"|echo }}% endif %{{ "}"|echo }}
            {% endif %}
        {% endif %}
    {% endfor %}
            WHERE {{key}} = #{ {{key}} }
        </value>
    </sql>
    <sql>
        <key>Delete</key>
        <value>
            DELETE FROM `{{table.Name}}` WHERE `{{key}}` = #{ {{key}} }
        </value>
    </sql>
</xml>
"""


# noinspection SpellCheckingInspection
def get_mapper_xml(database_info: DataBaseInfo, table_name: str) -> str:
    """
    Building XML with database description information
    :param database_info: Database description information
    :param table_name: Table name
    :return: XML document
    """

    # Template environment
    env = Environment()

    # Custom filter
    def echo(value):
        """
        Print a character for secondary rendering
        :param value: Characters to be printed
        :return: Original output
        """
        return value

    def clear_type(value):
        """
        Database type cleanup
        :param value:  Database type
        :return: Cleaning results
        """
        return value.split("(")[0]

    # Loading filter
    env.filters['echo'] = echo
    env.filters['clear_type'] = clear_type

    # Loading template
    template = env.from_string(_mapper_xml)

    # Assemble render parameters
    data = {"data_base_name": database_info["Name"]}

    # Lookup table information
    table = None
    for item in database_info["tables"]:
        if item["Name"] == table_name:
            table = item
            break
    if table is None:
        return ""
    data["table"] = table

    # Find primary key information
    key = ""
    for item in table["indexs"]:
        if item["Name"] == "PRIMARY":
            key = item["ColumnName"]
            break
    if key is None:
        return ""
    data["key"] = key

    # Load supported data types
    data["int_types"] = ["bit", "tinyint", "smallint", "mediumint", "int", "integer", "bigint"]
    data["float_types"] = ["real", "double", "float", "decimal", "numeric"]
    data["date_types"] = ["date", "time", "year", "timestamp", "datetime"]
    data["string_types"] = ["char", "varchar", "text", "mediumtext", "longtext"]

    return template.render(data)
