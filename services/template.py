"""
The following code is the only mandatory code for a service test


# This is needed if you want to log any errors
import logging
# This needs to be imported so the decorator and data can be used in the service test
from utils.settings import data, collect

# This needs to be above your function so the decorator can add it to a list for functional testing
@collect(data.get('services').get('YOUR_SERVICE_NAME_YOU_CREATED_IN_THE_JSON_FILE').get('enabled'))
def A_NAME_THAT_PERTAINS_TO_YOUR_SERVICE_TEST():
    # Get the configuration settings for your service
    # from config you may call config settings from main.json
    config = data.get('services').get('YOUR_SERVICE_NAME_YOU_CREATED_IN_THE_JSON_FILE')

    # Best practice to have error checking with logging
    #
    # try:
    #     a = 1/0
    # except:
    #     logging.exception("Oh no! you divided by 0")
    #

    # Have logic in your code to determine if the service is working
    return 0 # Return a 0 if it fails
    return 1 # Return a 1 if it passes
"""