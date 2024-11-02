###############################################################################
# Script to scrape Wisconsin voter registration data
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





###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://elections.wi.gov/statistics-data/voter-registration-statistics"

# PATH = '/Users/sinashaikh/Desktop/MEDSL/WI/registration/'
PATH = '/d/research/eln24/WI/registration/'

###############################################################################
# Global functions
###############################################################################
#Pause for an unpredictable duration while scraping
def pause(least):
    least = max(least, 2)
    time.sleep(max(0,np.random.randint(least-1,least)+np.random.uniform(0,1)))


def tryMakeDir(name, VERBOSE):
    try:
        os.makedirs(name)
    except:
        if VERBOSE:
            print(f"Writing to pre-existing folder: {name}")

def moveLatest(curr_month, curr_year):
    for file in os.listdir(PATH + '/quarantine/'):
        if not file.__contains__('.html'):
            file_path = PATH + f'{curr_year}_{curr_month}' + '.' + file.split('.', 1)[1]
            if not os.path.exists(file_path):
                os.rename(PATH + '/quarantine/' + file, file_path)


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

pathlib.Path(PATH+ '/quarantine').mkdir(parents=True, exist_ok=True)

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

while True:

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "views-row"))
    )

    links = []
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, " Voter Registration Statistics")

    for link in links:
        link_text = link.text # we do this because the link element no longer exists when we call move_latest
        link.click()
        if driver.find_elements('xpath', '//a[(contains(@href, "Ward") or contains(@href, "ward")) and (contains(@href, ".csv") or contains(@href, ".xls") or contains(@href, ".xlsx"))]'):
            driver.find_element('xpath', '//a[(contains(@href, "Ward") or contains(@href, "ward")) and (contains(@href, ".csv") or contains(@href, ".xls") or contains(@href, ".xlsx"))]').click()
        pause(5) #Long enough to finish the download for the largest file
        moveLatest(link_text.split(' ')[2], link_text.split(' ')[0])
        driver.back()
        pause(10)

    try:
        driver.get(driver.find_element(By.XPATH, "//a[@title='Go to next page']").get_attribute("href"))
    except NoSuchElementException:
        break

# Copy over to other folder for EPC dailies
OTHER_PATH = '/d/research/epc_dailies/infrastructure/reg/WI/raw/'

for file_name in os.listdir(PATH):
    if "2020" in file_name or "2024" in file_name:
        os.system(f"cp '{PATH + file_name}' '{OTHER_PATH}'")

print("WI registration scraper failed to retrieve stats on: " + CURR_DATE)
