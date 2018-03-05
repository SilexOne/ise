# TODO: For requriements.txt, virtualenv for dnspython
# TODO: Docstrings
# TODO: test working, some working some failing, all failing, create try blocks
# TODO: Implement logging
# TODO: Pass db connection to service main
# TODO: Take away the need for other programmers to use names like "dns"
import os
import json
from dns import resolver, reversename
from pprint import pprint # TODO: Delete when finished debugging

class domain_name_system():
	"""
	TODO: Docstrings
	"""
	def __init__(self, database, testing_against):
		"""
		TODO: Docstrings
		"""
		# Once this object is created have a new sqlite table created for the service
		database.init_table("dns")
		# We need to get the parent directory of this file
		# in order to import the config JSON for this service
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		# TODO: Based off the master config
		# This allows for individuals to test stuff locally
		# without constantly changing their production config
		self.verify_against = testing_against # This will be linked to the master config, ensure rest of json has testing, and production	
		# We need to open up the JSON file to pull the config data,
		# We use os library to join the parent directory with the 
		# JSON file which allows this to be run in Windows or Linux
		self.data = json.load(open(os.path.join(self.dir_path, __file__.split('.')[0] + '.json'))) # TODO: Change to get this files name with a .json behind it
		# Create the DNS reslover and associate a server
		# from the JSON data
		self.res = resolver.Resolver()
		self.res.nameservers = list(self.data.get(testing_against).get("dns").values()) # For SECCDC, it might only test main, TODO: Determine if it needs to test only main or both seperatly or combined

	def verify(self, item):
		"""
		TODO: Docstrings
		"""
		try:
			ip = str(self.res.query(item[0])[0].address)
			hostname = str(self.res.query(
				reversename.from_address(item[1]), 'PTR'
			)[0].target)[:-1]
			if self.data.get(self.verify_against).get('hostnames').get(hostname) == ip:
				return True
			else:
				return False
		except:
			return False


	def run(self, database):
		"""
		TODO: Docstrings
		"""
		# Determine if all the ips and hostnames are correct,
		# We do this by comparing the results from the JSON with
		# the DNS server were testing
		hostname_ip_pairs = [(key, value) for key, value in
			self.data.get(self.verify_against).get("hostnames").items()
		]
		result = [self.verify(pair) for pair in hostname_ip_pairs]
		sqlite_result = 1 if all(result) else 0

		database.commit_to_sqlite("dns", sqlite_result)
		database.query_last_service_db("dns") # TODO: Logging