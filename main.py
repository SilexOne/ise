# TODO: test working, some working some failing, all failing, create try blocks
# TODO: Implement logging
import sys # TODO: delete if not used
import time
import json
import logging
from datetime import datetime, timedelta
from os import path

from database import ise_db
from services import score_dns



def get_services(database, data):
	# Retrieve all the services
	using = data.get('services')
	
	# Determines if its testing or production so when the
	# services initialize it will use the appropriate settings
	verify_against = data.get('name')
	
	# Initialize all the serivces objects and return them to main
	services = []
	if using.get('dns'):
		services.append(score_dns.domain_name_system(database, verify_against))
	if using.get('ad'):
		services.append(score_ad.active_directory(database, verify_against))
	# TODO: Add the rest of the services
	return services

def main():
	# Set the logging settings
	formatting = '%(asctime)s [%(levelname)s]:%(message)s'
	logging.basicConfig(format=formatting, level=logging.INFO)

	# Get the contents from the main.json which will act as the config file
	data = json.load(
		open(path.abspath(__file__).split('.')[0] + '.json')
	).get("1")
	timeframe = data.get("timeframe")

	# Initialize an empty database
	database = ise_db.ise_database()
	logging.info("The ise.db was created")

	# Go through the config file and only enable the services set to on.
	# When the services are enabled their __init__ will create an empty 
	# table within the ise database, it will also determine if all the
	# services will use their production or testing config settins
	services = get_services(database, data)

	# Once the database is initialize and the tables have been created
	# we are now able to test the services
	finish_time = datetime.now() + timedelta(hours=timeframe.get("hours"), minutes=timeframe.get("minutes")) # TODO: Pull from config
	while(datetime.now() < finish_time):
		for service in services:
			# All services should have run() as their main, TODO: Find a better way
			service.run(database)
		time.sleep(5)

	# Once the appropriate amount of time has elapsed close the
	# connection to the database
	# TODO: Indicate end of scoring
	database.close_db() # TODO: Ensure the connection is closed

if __name__ == '__main__':
	main()