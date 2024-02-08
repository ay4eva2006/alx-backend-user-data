#!/usr/bin/env python3
"""0. Regex-ing 0. Regex-ing"""

import re
import logging
from typing import (
    List,
)
from mysql.connector.connection import MySQLConnection
import os


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        match = r'({}=)([^{}]+)'.format(field, separator)
        message = re.sub(match, r'\1{}'.format(redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=list(PII_FIELDS)))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """returns a connector to the database"""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    return MySQLConnection(user=username, password=password,
                           host=host, database=db_name)


def main():
    """
    Obtain a database connection using get_db and retrieve all
    rows in the users table and display each row under a filtered
    format
    """
    db = get_db()
    logger = get_logger()
    cur = db.cursor()
    cur.execute('SELECT * FROM users')
    for row in cur:
        logger.info(''.join('{}={}; '.format(name, value) for name,
                            value in zip(cur.column_names, row)))


if __name__ == '__main__':
    main()
