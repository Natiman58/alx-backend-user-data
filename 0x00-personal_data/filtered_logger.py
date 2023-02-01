#!/usr/bin/env python3

"""
    A filter module to hide some user data
"""


import re
from typing import List


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
