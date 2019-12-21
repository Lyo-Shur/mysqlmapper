import json


# 数据传输工具类
from datetime import datetime


class CodeModeDTO:
    # 状态码
    code = 0
    # 消息体
    message = ""
    # 数据体
    data = {}

    def __init__(self, code, message, data):
        """
        初始化状态传输工具类
        :param code: 状态码
        :param message: 消息体
        :param data: 数据体
        """
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        """
        转为Json对象
        :return:
        """
        if isinstance(self.data, datetime):
            return json.dumps({
                "code": self.code,
                "message": self.message,
                "data": self.data.strftime('%Y-%m-%d %H:%M:%S')
            }, ensure_ascii=False)
        if isinstance(self.data, tuple) or isinstance(self.data, list):
            for i in range(0, len(self.data)):
                if isinstance(self.data[i], datetime):
                    self.data[i] = self.data[i].strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(self.data, dict):
            for key in self.data.keys():
                if isinstance(self.data[key], datetime):
                    self.data[key] = self.data[key].strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps({"code": self.code, "message": self.message, "data": self.data}, ensure_ascii=False)
