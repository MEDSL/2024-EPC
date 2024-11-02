###############################################################################
# Script to scrape Pennsylvania voter registration data
###############################################################################

from datetime import datetime
import os
import requests

###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://www.pa.gov/content/dam/copapwp-pagov/en/dos/resources/voting-and-elections/voting-and-election-statistics/currentvotestats.xls"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/PA/registration/"
PATH = "/d/research/eln24/PA/registration/"


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
# try:
resp = requests.get(BASE_URL)
tryMakeDir(PATH, VERBOSE)
output = open(PATH+CURR_DATE+'.xls', 'wb')
output.write(resp.content)
output.close()

# Copy into another folder for the dailies
output = open("/d/research/epc_dailies/infrastructure/reg/PA/raw/"+CURR_DATE+'.xls', 'wb')
output.write(resp.content)
output.close


# Extra AVR file for Samuel
resp = requests.get("https://www.pavoterservices.pa.gov/AVR-Party-Breakdown.pdf")
tryMakeDir("/d/research/eln24/PA/AVR/", VERBOSE)
output = open("/d/research/eln24/PA/AVR/"+CURR_DATE+'.pdf', 'wb')
output.write(resp.content)
output.close()

# except:
#     print("PA registration scraper failed to retrieve stats on: " + CURR_DATE)

