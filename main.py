import time
import logging
import sse_logging  # TODO: Implement logging the right way
from datetime import datetime, timedelta
from settings import scoring, data
from database import sse_db
from services import score_dns  # TODO: Find a better way


def main():
    logging.info("Service Scoring Engine started")

    # Using the json configuration settings from the global variable
    # get the time frame in which the scoring engine will run
    scoring_duration = data.get("timeframe")

    # Initialize a sqlite3 database
    database = sse_db.SqliteDatabase()

    # Initialize all the tables in the database
    for service in scoring:
        database.init_table(service.__name__)

    # Get the finish time of the scoring test
    finish_time = datetime.now() + timedelta(hours=scoring_duration.get("hours"),
                                             minutes=scoring_duration.get("minutes"))

    # Once the database is initialized and the tables have been created
    # we are now able to test the services until the finish time
    while datetime.now() < finish_time:
        for service in scoring:
            try:
                database.commit_to_sqlite(service.__name__, service())
            except:
                logging.exception("Service test function failed: {}".format(service.__name__))
        time.sleep(5)  # TODO: Find better way

    # Once the appropriate amount of time has elapsed close the
    # connection to the database
    # TODO: Indicate end of scoring
    database.close_db()  # TODO: Ensure the connection is closed
    logging.info("Service Scoring Engine has finished")


if __name__ == '__main__':
    main()
