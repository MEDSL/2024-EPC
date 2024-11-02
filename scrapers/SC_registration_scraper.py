###############################################################################
# Script to scrape South Carolina voter registration data
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
from selenium.webdriver.support.ui import Select
import pathlib


###############################################################################
# Global variables
###############################################################################
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jun', 'Jul',
          'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://vrems.scvotes.sc.gov/Statistics/CountyAndPrecinct"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/SC/registration/"
PATH = '/d/research/eln24/SC/registration/'



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

driver.get(BASE_URL)

try:
    WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "Demographic"))
        )

    county_dropdown = Select(driver.find_element(By.ID, "CountySID"))
    demographic_dropdown = Select(driver.find_element(By.ID, "Demographic"))


    for county in county_dropdown.options[1:]:
        for demographic in demographic_dropdown.options[1:]:
            county_dropdown.select_by_visible_text(county.text)
            demographic_dropdown.select_by_visible_text(demographic.text)
            driver.find_element(By.ID, "viewResults").click()
            pause(1)
            driver.find_element(By.PARTIAL_LINK_TEXT, "Export").click()
    

    pause(10)


            
    driver.quit()

    # Copy over to other folder for EPC dailies
    OTHER_PATH = '/d/research/epc_dailies/infrastructure/reg/SC/raw/'

    for file_name in os.listdir(PATH):
        if not os.path.exists(OTHER_PATH + file_name):
            os.system(f"cp '{PATH + file_name}' '{OTHER_PATH}'")

except:
    print("SC registration scraper failed to retrieve stats on: " + CURR_DATE)
