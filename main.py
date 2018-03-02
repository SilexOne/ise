import os

from database import ise_db
from services import score_dns


def main():
	dir_path = os.path.dirname(os.path.realpath(__file__)) # TODO: Determine if this is needed
	database = ise_db.ise_database()
	database.init_db()

	# TODO: Get the remaining services
	# TODO: Use hyperthreading for
	dns = score_dns.domain_name_system() # TODO: Pass database object
	dns.run_dns_service(database)

	database.close_db()

if __name__ == '__main__':
	main()