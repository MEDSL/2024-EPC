###############################################################################
# Script to scrape North Carolina voter registration data
###############################################################################
import time
from datetime import datetime
import numpy as np
import pathlib
import csv
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
'''


###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://www.ncsbe.gov/results-data/absentee-and-provisional-data"

PATH = '/d/research/eln24/NC/early/'
ALT_PATH = '/d/research/epc_dailies/infrastructure/early/NC/raw/'


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
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

params = {'behavior' : 'allow', 'downloadPath' : PATH + '/quarantine'}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)


###############################################################################
# Scrape
###############################################################################
driver.get(BASE_URL)
pause(1)

links = driver.find_elements(By.PARTIAL_LINK_TEXT,
        "2024 Nov 05 Election - Absentee Statewide (ZIP)")

for link in links:
    download_file_if_not_exists(link.get_attribute("href"))

driver.quit()

pause(30)


###############################################################################
# Copy out of folder
###############################################################################
quarantined = os.listdir(PATH+'quarantine/')
for fname in quarantined:
    os.rename()

















