###############################################################################
# Script to scrape New Hampshire voter registration data
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
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://www.sos.nh.gov/party-registration-history-1970-2024"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/NH/registration/"
PATH = '/d/research/eln24/NH/registration/'


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
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


params = {'behavior' : 'allow', 'downloadPath' : PATH}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

###############################################################################
# Scrape
###############################################################################

try:
    driver.get(BASE_URL)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "logo-header"))
    )

    links = driver.find_elements(By.CLASS_NAME, "file--mime-application-vnd-openxmlformats-officedocument-spreadsheetml-sheet")

    for link in links:
        driver.get(link.get_attribute("href"))
        pause(5)


    driver.quit()
except:
    print("NH registration scraper failed to retrieve stats on: " + CURR_DATE)
