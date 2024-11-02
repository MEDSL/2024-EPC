###############################################################################
# Script to scrape Pennsylvania Early Data
###############################################################################
import time
from datetime import datetime, timedelta
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

from os import rename



###############################################################################
# Global variables
####################################################################s###########
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://copaftp.state.pa.us/Web/Account/Login.htm"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/PA/early/"
PATH = '/d/research/eln24/PA/early/'



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
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
}
options.add_experimental_option("prefs", prefs)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


###############################################################################
# Scrape
###############################################################################

try:
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    pause(3)

    driver.find_element(By.ID, "username").send_keys("ST-DOSFTP5A")
    driver.find_element(By.ID, "password").send_keys("JQTxnEV4")
    driver.find_element(By.ID, "loginSubmit").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mat-checkbox-1-input"))
    )

    pause(2)

    driver.find_elements(By.CSS_SELECTOR, ".mat-checkbox-inner-container")[2].click()
    pause(2)
    driver.find_elements(By.CSS_SELECTOR, ".mat-checkbox-inner-container")[3].click()
    pause(2)
    
    driver.find_element(By.XPATH, "//span[text()='Download']").click()
    
    pause(500)

    # Copy over to other folder for EPC dailies
    OTHER_PATH = '/d/research/epc_dailies/infrastructure/early/PA/raw/'

    for file_name in os.listdir(PATH):
        if not os.path.exists(OTHER_PATH + file_name):
            os.system(f"cp '{PATH + file_name}' '{OTHER_PATH}'")


    



except Exception as e:
    print(f"PA early scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()
