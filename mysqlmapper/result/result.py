import json


# Data transmission tool class
from datetime import datetime


class CodeModeDTO:
    # Status code
    code = 0
    # Message body
    message = ""
    # Data volume
    data = {}

    def __init__(self, code, message, data):
        """
        Initialization status transfer tool class
        :param code: Status code
        :param message: Message body
        :param data: Data volume
        """
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        """
        Convert to JSON object
        :return:
        """
        self.data = self._parse_time(self.data)
        return json.dumps({
            "code": self.code,
            "message": self.message,
            "data": self.data
        })

    def _parse_time(self, data):
        """
        Recursive processing time format
        :param data: Data to be processed
        :return: Processing result
        """
        if isinstance(data, datetime):
            data = data.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(data, tuple) or isinstance(data, list):
            for i in range(0, len(data)):
                data[i] = self._parse_time(data[i])
        if isinstance(data, dict):
            for key in data.keys():
                data[key] = self._parse_time(data[key])
        return data
