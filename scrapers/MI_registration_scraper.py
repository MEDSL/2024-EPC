###############################################################################
# Script to scrape Michigan voter registration data
###############################################################################

from datetime import datetime
import os
import requests

###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://mvic.sos.state.mi.us/VoterCount/DownloadFile?Length=10"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/MI/registration/"
PATH = "/d/research/eln24/MI/registration/"
PATH_OTHER = "/d/research/epc_dailies/infrastructure/reg/MI/raw/"

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
try:
    # Get data
    resp = requests.get(BASE_URL)

    # Make directory if it doesn't exist only for general elec data
    tryMakeDir(PATH, VERBOSE)

    # Save to general election data folder
    output = open(PATH+CURR_DATE+'.txt', 'wb')
    output.write(resp.content)
    output.close()

    # Save to folder for EPC Dailies
    output = open(PATH_OTHER+CURR_DATE+'.txt', 'wb')
    output.write(resp.content)
    output.close()
except:
    print("MI registration scraper failed to retrieve stats on: " + CURR_DATE)

