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
import mysql.connector
import os

# Get environment variables
USER = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
HOST = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
DB_NAME = os.getenv('PERSONAL_DATA_DB_NAME')

# Tuple constant for the PII files
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    """
        Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formater class using the given fields"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ return filtered(obfuscated) values from incoming log records """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.logger obj"""
    logger = logging.getLogger("user_data")  # set the logger
    logger.setLevel(logging.INFO)  # set the logger level
    logger.propagate = False  # no need to propagate to other loggers

    handler = logging.StreamHandler()  # set the handler
    formatter = RedactingFormatter(PII_FIELDS)  # set the formatter
    handler.setFormatter(formatter)  # add the formatter to the handler
    logger.addHandler(handler)  # add the handler to the logger object

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns connector to the database"""
    return mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DB_NAME
    )


def main() -> None:
    """
        retrieve all rows in the database
        and obfuscate the coulmns
        (name, email, phone, ssn, password)
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    column = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(column, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
