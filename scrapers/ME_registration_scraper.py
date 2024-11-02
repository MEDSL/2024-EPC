###############################################################################
# Script to scrape Maine voter registration data
# Note further information is available at the BASE_URL
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
import requests

from os import rename



###############################################################################
# Global variables
###############################################################################
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://www.maine.gov/sos/cec/elec/data/index.html"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/ME/registration/"
PATH = '/d/research/eln24/ME/registration/'



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
        if ".txt" in file_name:
            with open(file_path, 'wb') as file:
                file.write(requests.get(url).content)
        else: 
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
    pause(1)

    links = driver.find_elements(By.LINK_TEXT, "Statewide Registered and Enrolled Data File")

    for link in links:
        download_file_if_not_exists(link.get_attribute("href"))

    driver.get("https://www.maine.gov/sos/cec/elec/data/prevregandenroll.html")

    links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Statewide Registered and Enrolled Data File")

    for link in links:
        if ".html" not in link.get_attribute("href") and ".pdf" not in link.get_attribute("href"):
            download_file_if_not_exists(link.get_attribute("href"))





except Exception as e:
    print(f"ID registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()