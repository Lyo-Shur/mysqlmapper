

class Engine:
    """
    SQL执行引擎
    """
    @staticmethod
    def query(conn, sql, parameter):
        """
        查询列表信息
        :param conn: 数据库连接
        :param sql: 待执行的SQL语句
        :param parameter: 参数
        :return: 查询结果
        """
        # 获取游标
        cursor = conn.cursor()
        # 执行SQL
        cursor.execute(sql, parameter)
        # 提交操作
        conn.commit()
        # 获取表头
        names = []
        for i in cursor.description:
            names.append(i[0])
        # 获取结果集
        results = []
        for i in cursor.fetchall():
            result = {}
            for j in range(len(i)):
                result[names[j]] = i[j]
            results.append(result)
        cursor.close()
        return results

    @staticmethod
    def count(conn, sql, parameter):
        """
        查询数量信息
        :param conn: 数据库连接
        :param sql: 待执行的SQL语句
        :param parameter: 参数
        :return: 查询结果
        """
        result = Engine.query(conn, sql, parameter)
        if len(result) == 0:
            return 0
        for value in result[0].values():
            return value

    @staticmethod
    def exec(conn, sql, parameter):
        """
        执行SQL语句
        :param conn: 数据库连接
        :param sql: 待执行的SQL语句
        :param parameter: 参数
        :return: 最后一次插入ID，影响行数
        """
        # 获取游标
        cursor = conn.cursor()
        # 执行SQL
        cursor.execute(sql, parameter)
        # 提交操作
        conn.commit()
        # 影响行数
        rowcount = cursor.rowcount
        # 最后一次插入ID
        lastrowid = cursor.lastrowid
        # 关闭游标
        cursor.close()
        return lastrowid, rowcount
