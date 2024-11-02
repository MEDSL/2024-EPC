###############################################################################
# Script to scrape Florida vote by mail data
###############################################################################
import time
from datetime import datetime
import numpy as np
import pathlib
import csv
import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


###############################################################################
# Global variables
###############################################################################
VERBOSE = True

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://countyballotfiles.floridados.gov/VoteByMailEarlyVotingReports/PublicStats"

PATH = '/d/research/eln24/FL/vbm/'
ALT_PATH = '/d/research/epc_dailies/infrastructure/early/FL/raw/'


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
params = {'behavior' : 'allow', 'downloadPath' : PATH}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)


###############################################################################
# Scrape
###############################################################################
driver.get(BASE_URL)

#First find all the links to download files, and download them
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Download File"))
)
links = driver.find_elements(By.PARTIAL_LINK_TEXT,
        "Download File")
pause(2)
for link in links:
    download_file_if_not_exists(link.get_attribute("href"))
    pause(20)

#Also write down the data that they've put into the website, which may not
# match the data that's in the files linked on the website
table = driver.find_element('id', 'statewideTotal')
webText = table.text
with open(f"{PATH}{CURR_DATE}_WebData.txt", "w+") as f:
    f.write(webText)

driver.quit()


###############################################################################
# Save location and name
###############################################################################
#Change the name of any files not yet in date format into the date format
allfnames = os.listdir(PATH)
for fname in allfnames:
    if 'EarlyVoted' in fname:
        os.rename(f"{PATH}{fname}", f"{PATH}{CURR_DATE}_early.txt")
    if 'VbmProvided' in fname:
        os.rename(f"{PATH}{fname}", f"{PATH}{CURR_DATE}_provided.txt")
    elif 'VbmVoted' in fname:
        os.rename(f"{PATH}{fname}", f"{PATH}{CURR_DATE}_voted.txt")

#Copy to the epc_dailies directory as well
curfnames = os.listdir(PATH)
altfnames = os.listdir(f"{ALT_PATH}files/")
for fname in curfnames:
    if fname not in altfnames:
        if 'WebData' in fname:
            shutil.copyfile(f"{PATH}{fname}", f"{ALT_PATH}{fname}")
        else:
            shutil.copyfile(f"{PATH}{fname}", f"{ALT_PATH}files/{fname}")
