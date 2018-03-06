# TODO: test working, some working some failing, all failing, create try blocks
# TODO: Implement logging
# TODO: Docstrings
import sqlite3
import shutil
import sys # TODO: Delete id not used
from os import path
from datetime import datetime


# TODO: Called from main, to setup the the sqlite database
class ise_database():
	"""
	TODO: Docstrings
	"""
	def __init__(self):
		"""
		TODO: Docstrings
		"""
		# Move the database into the backup folder, and make a new database
		self.dir_path = path.dirname(path.realpath(__file__))
		self.abs_path = path.join(self.dir_path, 'ise.db')
		self.new_abs_file_path = path.join(path.join(path.dirname(self.dir_path), "backup"), str(datetime.now().strftime('%Y-%m-%dT%H-%M-%S') + '.db'))
		try:
			shutil.move(self.abs_path, self.new_abs_file_path)
		except OSError as e:
			# TODO: Find a better way
			pass
		self.connection = sqlite3.connect(self.abs_path)
		self.cursor = self.connection.cursor()

	def init_table(self, service):
		"""
		TODO: Docstrings
		"""
		# TODO: Have the main config only create those being used
		"""
		|      id       |   epoch    | status |
		|---------------|------------|--------|
		| 1             | 1519939251 |   0    |
		| 2             | 1519939263 |   0    |
		| 3             | 1519939279 |   1    |
		"""
		sql_command = """
			CREATE TABLE IF NOT EXISTS {} (
			id INTEGER PRIMARY KEY,
			epoch timestamp DEFAULT (strftime('%s', 'now')),
			status INTEGER);""".format(service)
		self.cursor.execute(sql_command) # TODO: Logging


	def commit_to_sqlite(self, service, status):
		"""
		TODO: Docstrings
		"""
		sql_command = """
			INSERT INTO {0} (status)
		    VALUES ({1});""".format(service, status)
		self.cursor.execute(sql_command)
		self.connection.commit() # TODO: Logging

	def query_service_db(self, service):
		"""
		TODO: Docstrings
		"""
		self.cursor.execute("SELECT * FROM {}".format(service))
		all_rows = self.cursor.fetchall()
		for row in all_rows:
			print('{0} | {1} | {2}'.format(row[0], row[1], row[2]))

	def query_last_service_db(self, service):
		"""
		TODO: Docstrings
		"""
		self.cursor.execute("SELECT * FROM {}".format(service))
		all_rows = self.cursor.fetchall()
		print('{0} | {1} | {2}'.format(all_rows[-1][0], all_rows[-1][1], all_rows[-1][2]))

	def close_db(self):
		"""
		TODO: Docstrings
		"""
		self.connection.close()