# TODO: test working, some working some failing, all failing, create try blocks
# TODO: Implement logging in another file
import time
import logging
from datetime import datetime, timedelta
from settings import scoring, data
from database import ise_db
from services import score_dns # TODO: Find a better way


def main():
    # TODO: Logging will have its own file
    # Set the logging settings
    formatting = '%(asctime)s [%(levelname)s]: %(message)s'
    logging.basicConfig(format=formatting, level=logging.INFO)

    # Using the json configuration settings from the global variable
    # get the time frame in which the scoring engine should run
    scoring_duration = data.get("timeframe")

    # Initialize a sqlite3 database
    database = ise_db.sqlite_database()

    # Initialize all the tables for the database
    for service in scoring:
        database.init_table(service.__name__)

    # Get the finish time of the scoring test
    finish_time = datetime.now() + timedelta(hours=scoring_duration.get("hours"),
                                             minutes=scoring_duration.get("minutes"))

    # Once the database is initialize and the tables have been created
    # we are now able to test the services until the finish time
    while (datetime.now() < finish_time):
        for service in scoring:
            database.commit_to_sqlite(service.__name__, service())
        time.sleep(5)  # TODO: Find better way

    # Once the appropriate amount of time has elapsed close the
    # connection to the database
    # TODO: Indicate end of scoring
    database.close_db()  # TODO: Ensure the connection is closed
    logging.info("ISE finished")


if __name__ == '__main__':
    main()
