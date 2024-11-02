###############################################################################
# Script to scrape West Virginia voter registration data
###############################################################################
import time
from datetime import datetime
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pathlib


###############################################################################
# Global variables
###############################################################################
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jun', 'Jul',
          'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://sos.wv.gov/elections/Documents/VoterRegistrationTotals/"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/WV/registration/"
PATH = '/d/research/eln24/WV/registration/'



###############################################################################
# Global functions
###############################################################################
def tryMakeDir(name, VERBOSE):
    try:
        os.makedirs(name)
    except:
        if VERBOSE:
            print(f"Writing to pre-existing folder: {name}")

def pause(least):
    least = max(least, 2)
    time.sleep(max(0,np.random.randint(least-1,least)+np.random.uniform(0,1)))




###############################################################################
# Setup
###############################################################################


pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)

options = Options()

prefs = {
    "plugins.always_open_pdf_externally": True,  # Download PDF instead of opening in the browser
    "download.default_directory": PATH,  # Specify your download directory
    "download.prompt_for_download": False,  # Disable the download prompt
}
options.add_experimental_option("prefs", prefs)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


###############################################################################
# Scrape
###############################################################################

try:
    for year in range(2016, datetime.today().year + 1):
        for month in MONTHS:   
            driver.get(f'{BASE_URL}/{year}/{month}{year}.pdf')
        
    driver.quit()
except:
    print("MD registration scraper failed to retrieve stats on: " + CURR_DATE)
