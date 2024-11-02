###############################################################################
# Script to scrape Louisiana voter registration data
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
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://www.sos.la.gov/ElectionsAndVoting/Pages/RegistrationStatisticsParish.aspx"

PATH = "/Users/sinashaikh/Desktop/MEDSL/LA/registration/"
# PATH = '/d/research/eln24/LA/registration/'



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

# try:
driver.get(BASE_URL)
driver.switch_to.frame("QueryStringPageViewer_ctl00$ctl34$g_04665f4c_f181_417e_a8cf_884f1b8fa02e")

WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "cboYear"))
)

year_dropdown = Select(driver.find_element(By.ID, "cboYear"))

year_texts = []

for year in year_dropdown.options:
    year_texts.append(year.text)

for year_text in year_texts:
    driver.get(BASE_URL)
    driver.switch_to.frame("QueryStringPageViewer_ctl00$ctl34$g_04665f4c_f181_417e_a8cf_884f1b8fa02e")
    year_dropdown = Select(driver.find_element(By.ID, "cboYear"))
    year_dropdown.select_by_visible_text(year_text)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "xls"))
    )

    links = driver.find_elements(By.PARTIAL_LINK_TEXT, "xls")

    link_hrefs = []

    for link in links:
        link_hrefs.append(link.get_attribute("href"))


    for link_href in link_hrefs:
        download_file_if_not_exists(link_href)
    

# except Exception as e:
#     print(f"LA registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

# finally:
#     driver.quit()