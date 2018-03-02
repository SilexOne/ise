# TODO: test working, some working some failing, all failing, create try blocks
# TODO: Implement logging
import sqlite3


# TODO: Called from main, to setup the the sqlite database
class ise_database():
	def __init__(self):
		self.connection = None
		self.cursor = None

	def init_db(self):
		# TODO: delete any databases in the folder
		self.connection = sqlite3.connect("ise.db") # TODO: ise.db, TODO: absoulte path needed when main uses this
		self.cursor = self.connection.cursor()

		# TODO: Have the main config only create those being used
		"""
		|      id       |   epoch    | status |
		|---------------|------------|--------|
		| 1             | 1519939251 |   0    |
		| 2             | 1519939263 |   0    |
		| 3             | 1519939279 |   1    |
		"""
		sql_command = """
			CREATE TABLE IF NOT EXISTS dns (
			id INTEGER PRIMARY KEY,
			epoch timestamp DEFAULT (strftime('%s', 'now')),
			status INTEGER);"""
		self.cursor.execute(sql_command) # TODO: Logging


	def commit_to_sqlite(self, service, status):
		sql_command = """
			INSERT INTO {0} (status)
		    VALUES ({1});""".format(service, status)
		self.cursor.execute(sql_command)
		self.connection.commit() # TODO: Logging

	def query_service_db(self, service):
		self.cursor.execute("SELECT * FROM dns".format(service))
		all_rows = self.cursor.fetchall()
		for row in all_rows:
			print('{0} | {1} | {2}'.format(row[0], row[1], row[2]))

	def close_db(self):
		self.connection.close()


# TODO: Delete when finished
if __name__ == '__main__':
	a = ise_database()
	a.init_db()
	a.commit_to_sqlite("dns", 1)
	a.query_service_db("dns")
	a.close_db()