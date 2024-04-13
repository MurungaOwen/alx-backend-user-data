#!/usr/bin/env python3
"""module to define filter_datum"""
import typing as t
import re
import logging
import mysql.connector
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: t.List, redaction: str,
                 message: str, separator: str) -> str:
    """obfuscates a log message"""
    for field in fields:
        message = re.sub(field + '=(.*?);',
                         field + '=' + redaction + separator, message)

    return message


def get_logger() -> logging.Logger:
    """return a logging .Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    s_handler = logging.StreamHandler()
    s_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(s_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects to a sql database"""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    conn = mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return conn


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: t.List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filters a string of incomming logs"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def main():
    """main function"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
