# TODO: test working, some working some failing, all failing, create try blocks
# TODO: Implement logging
import sys # TODO: delete if not used
import threading
import time
import json
from datetime import datetime, timedelta
from os import path # TODO: delete if not used

from database import ise_db
from services import score_dns

def get_services(database, data):
	using = data.get('services')
	verify_against = data.get('name')
	services = []
	if using.get('dns'):
		services.append(score_dns.domain_name_system(database, verify_against))
	if using.get('ad'):
		services.append(score_ad.active_directory(database, verify_against))
	return services

def main():
	# Get the contents from the main.json which will act as the config file
	# Any change to the settings may be edited in main.json
	data = json.load(
		open(path.abspath(__file__).split('.')[0] + '.json')
	).get("1")

	# Initialize an empty database
	database = ise_db.ise_database()

	# Go through the config file and only enable the services set to on.
	# When the services are enabled their __init__ will create an empty 
	# table within the ise database, it will also determine if all the
	# services will use their production or testing config settins
	services = get_services(database, data)

	# Once the database is initialize and the tables have been created
	# we are now able to test the services
	finish_time = datetime.now() + timedelta(hours=0, minutes=1) # TODO: Pull from config
	while(datetime.now() < finish_time):
		for service in services:
			# All services should have run() as their main
			service.run(database)
		time.sleep(5)

	# Once the appropriate amount of time has elapsed close the
	# connection to the database
	# TODO: Indicate end of scoring
	database.close_db() # TODO: Ensure the connection is closed

if __name__ == '__main__':
	main()