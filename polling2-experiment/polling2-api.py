"""
This file is for testing out polling2 as a means to poll an API, manipulate the response, and repeat.

It uses the SWAPI test API endpoint.
Have a look at this URL to see what we're pulling down: https://swapi.dev/api/people/1
"""

import datetime
import requests
import polling2
import logging
import json

### Config ###
WAIT_TIME_S = 5  # Time in seconds to wait between each API call
REPEAT_AMOUNT = 3  # How many times to run this API call/poll
# See bottom of this file for how to poll forever
##############

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def checker(response):
    # always return False, which will make the polling engine never end, unless interrupted by timeout or max_tries.
    return False


def get_people():
    logging.info("----------")
    response = requests.get('https://swapi.dev/api/people/1', verify=False)
    logging.info("Received Response Code: " + str(response.status_code) + " " + str(response.reason))
    logging.debug("Received Response: \n" + str(response.content))

    response_json = json.loads(response.text)  # Marshall the json text into a Python json object
    edited = response_json["edited"]  # "edited":"2014-12-20T21:17:56.891000Z"

    # Calculate the time difference between now and the "edited" date field
    edited_date = datetime.datetime.strptime(edited.split('.')[0], DATE_FORMAT)
    difference_date = datetime.datetime.now() - edited_date
    logging.info("Time difference is " + str(difference_date))

    if difference_date > datetime.timedelta(minutes=2):
        logging.warning("Hey this is a really old record!")
    logging.info("==========")
    return response


logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

polling2.poll(
    get_people,
    check_success=checker,
    step=WAIT_TIME_S,  # repeat every n seconds
    max_tries=REPEAT_AMOUNT,  # repeat n times
    # poll_forever=True  # repeat forever. pick this or max_tries
    # ignore_exceptions=(requests.exceptions.ConnectionError,),  # can be used to ensure exceptions don't stop polling, such as failed connections
    log=logging.DEBUG
)
