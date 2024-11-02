###############################################################################
# Script to scrape Vermont voter registration data
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
import csv


###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://sos.vermont.gov/voter-registration-stats/"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/VT/registration/"
PATH = "/d/research/eln24/VT/registration/"

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
# Scrape
###############################################################################

try:
    driver.get(BASE_URL)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )

    table = driver.find_elements(By.TAG_NAME, 'table')[2]

    table_data = []

    headers = [header.text.strip() for header in table.find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')]
    table_data.append(headers)


    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text.strip() for cell in cells]
        if row_data:
            table_data.append(row_data)


    with open(PATH + f'{datetime.today().month}_{datetime.today().year}', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)

    driver.quit()
except:
    print("VT registration scraper failed to retrieve stats on: " + CURR_DATE)
