#!/usr/bin/env python3

"""
    A filter module to hide some user data
    if RE <.*> is matched against '<a> b <c>',
    it will match the entire string, and not just '<a>'.
    Adding ? after the quantifier makes it perform the match
    in non-greedy or minimal fashion; as few characters as
    possible will be matched. Using the RE <.*?> will match only '<a>'.
"""


import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns an obfuscated message
    :param fields: list of fields to be obfuscated
    :message: the log message
    :separator: the separator
    """
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialize the formater class using the given fields"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            return filtered values from incoming log records
            using filter_datum functon
            fields = ["password", "date_of_birth"]
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)
