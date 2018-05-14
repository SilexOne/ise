import json
import os

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
        if enabled:
            scoring.append(func)
    return real_decorator

# Get the contents from the main.json which will act as the config file
data = json.load(open(os.path.join(os.getcwd(), 'main.json'))).get("1")
