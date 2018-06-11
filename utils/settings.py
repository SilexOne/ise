import os
import sys
import json
import logging
# Create a global variable that can be passed to other
# files so collect and can add functions to it
global scoring
global data
scoring = []
data = {}

# Make this a decorator on all services so the
# function can be added to the global variable
def collect(enabled):
    def real_decorator(func):
        if not(enabled == 0 or enabled == 1):
            logging.exception("The decorator argument on {} service function must be either a 1 or 0, "
                              "check the JSON configuration file to ensure that it\'s correct".format(func.__name__))
            sys.exit()
        if enabled:
            scoring.append(func)
    return real_decorator

# Get the contents from the main.json which will act as the config file
data = json.load(open(os.path.join(os.getcwd(), 'main.json'))).get("1")
