###############################################################################
# Script to scrape North Carolina voter registration data
###############################################################################

from datetime import datetime
import os
import requests


###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/NC/registration/"
PATH = "/d/research/eln24/NC/registration/"


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
    resp = requests.get(BASE_URL)
    

    tryMakeDir(PATH, VERBOSE)
    output = open(PATH+CURR_DATE+'.zip', 'wb')
    output.write(resp.content)
    output.close()
    
    # Also write to epc_dailies folder
    output = open("/d/research/epc_dailies/infrastructure/reg/NC/raw/"+CURR_DATE+'.zip', 'wb')
    output.write(resp.content)
    output.close()

except:
    print("NC registration scraper failed to retrieve stats on: " + CURR_DATE)

