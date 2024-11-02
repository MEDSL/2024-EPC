###############################################################################
# Script to scrape Pennsylvania mail in ballot data
###############################################################################

from datetime import datetime
import os
import requests


###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://www.pavoterservices.pa.gov/2024%20Primary%20Daily%20Mail%20Ballot%20Report.xlsx"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/PA/mail/"
PATH = "/d/research/eln24/PA/mail/"

###############################################################################
# Global functions
###############################################################################
def tryMakeDir(name, VERBOSE):
    try:
        os.makedirs(name)
    except:
        if VERBOSE:
            print(f"Writing to pre-existing folder: {name}")

###############################################################################
# Scrape
###############################################################################

if datetime.today().month >= 9 or datetime.today().year > 2024:
    try:
        resp = requests.get(BASE_URL)

        tryMakeDir(PATH, VERBOSE)
        output = open(PATH+CURR_DATE+'.xls', 'wb')
        output.write(resp.content)
        output.close()
    except:
        print("PA mail scraper failed to retrieve stats on: " + CURR_DATE)

