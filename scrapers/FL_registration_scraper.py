###############################################################################
# Script to scrape Florida voter registration data
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

from os import rename



###############################################################################
# Global variables
###############################################################################
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://dos.fl.gov/elections/data-statistics/voter-registration-statistics/voter-registration-reports/"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/FL/registration/"
PATH = '/d/research/eln24/FL/registration/'



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

    link = driver.find_element(By.PARTIAL_LINK_TEXT, "County and Party - Excel")

    download_file_if_not_exists(link.get_attribute("href"))


    pause(5)
    
    # Copy over to other folder for EPC dailies
    OTHER_PATH = '/d/research/epc_dailies/infrastructure/reg/FL/raw/'

    for file_name in os.listdir(PATH):
        if file_name.endswith('.xlsx'):
            os.system(f"cp '{PATH + file_name}' '{OTHER_PATH}'")


    more_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Zip")

    for link in more_links:
        download_file_if_not_exists(link.get_attribute("href"))


except Exception as e:
    print(f"FL registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()
