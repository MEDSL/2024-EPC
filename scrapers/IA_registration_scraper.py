###############################################################################
# Script to scrape Iowa voter registration data
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
from selenium.common.exceptions import NoSuchElementException
import pathlib
import csv


###############################################################################
# Global variables
###############################################################################
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'April', 'May', 'Jun', 'June', 'Jul', 'July'
          'Aug', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://sos.iowa.gov/elections/pdf/VRStatsArchive/"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/IA/registration/"
PATH = '/d/research/eln24/IA/registration/'



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


def download_file_if_not_exists(url):
    file_name = url.split("/")[-1]
    file_path = os.path.join(PATH, file_name)
    if not os.path.exists(file_path):
        driver.get(url)
        pause(2)
    else:
        if VERBOSE:
            print(f"File already exists: {file_name}")

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
    driver.get(BASE_URL)

    for year in range(2000, datetime.today().year + 1):
        for month in MONTHS:
            download_file_if_not_exists(f'{BASE_URL}{year}/Co{month}{str(year)[-2:]}.pdf')
            pause(3)


except Exception as e:
    print(f"IA registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()


