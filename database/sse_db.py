import sys
import sqlite3
import shutil
import logging
from os import path
from datetime import datetime


class SqliteDatabase:

    def __init__(self):
        """
        This class initializes a SQLite3 database while moving any
        database named ise.db to a backup folder and stores the connection
        into the class attributes
        """
        # Move the database into the backup folder, and make a new database
        self.dir_path = path.dirname(path.realpath(__file__))
        self.abs_path = path.join(self.dir_path, 'sse.db')
        self.new_abs_file_path = path.join(path.join(path.dirname(self.dir_path), "backup"),
                                           str(datetime.now().strftime('%Y-%m-%dT%H-%M-%S') + '.db'))
        try:
            shutil.move(self.abs_path, self.new_abs_file_path)
        except OSError:
            pass
        try:
            self.connection = sqlite3.connect(self.abs_path)
            self.cursor = self.connection.cursor()
        except:
            logging.exception("Failed to make a connection to the database")
            sys.exit()
        logging.info("The database sse.db was created")

    def init_table(self, service):
        """
        Create a table within the database

        :param service: Name of the table to be created
        """
        # The table structure created
        # |      id       |   epoch    | status |
        # |---------------|------------|--------|
        # | 1             | 1519939251 |   0    |
        # | 2             | 1519939263 |   0    |
        # | 3             | 1519939279 |   1    |
        sql_command = """
            CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY,
            epoch timestamp DEFAULT (strftime('%s', 'now')),
            status INTEGER);""".format(service)
        try:
            self.cursor.execute(sql_command)
            logging.info("Created the {} table".format(service))
        except:
            logging.exception("Unable to create the {} table".format(service))

    def commit_to_sqlite(self, service, status):
        """
        Insert a value of a 0 or 1 (PASS/FAIL) into the status column of a service table,
        the id and time will be added automatically

        :param service: Table name in the database
        :param status: An integer return status from a service test of either a 0 or 1
        """
        sql_command = """
            INSERT INTO {0} (status)
            VALUES ({1});""".format(service, status)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            logging.debug("Inserted result of {} into the {} table".format(status, service))
        except:
            logging.exception("Unable to insert result of {} into the {} table".format(status, service))

    def query_service_table(self, service):
        """
        Query an entire table from the database

        :param service: Name of table to query from
        """
        try:
            self.cursor.execute("SELECT * FROM {}".format(service))
            all_rows = self.cursor.fetchall()
            for row in all_rows:
                print('{0} | {1} | {2}'.format(row[0], row[1], row[2]))
        except:
            logging.exception("Unable to SELECT * FROM {}".format(service))

    def query_last_service_table(self, service):
        """
        Query the last entry in the table

        :param service: Name of table to query from
        """
        try:
            self.cursor.execute("SELECT * FROM {}".format(service))
            all_rows = self.cursor.fetchall()
            print('{0} | {1} | {2}'.format(all_rows[-1][0], all_rows[-1][1], all_rows[-1][2]))
        except:
            logging.exception("Unable to SELECT * FROM {}".format(service))

    def close_db(self):
        self.connection.close()
        logging.info("Database connection closed")
