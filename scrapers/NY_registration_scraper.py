###############################################################################
# Script to scrape New York voter registration data
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
import requests


###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://elections.ny.gov/enrollment-election-district?page=0"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/NY/registration/"
PATH = '/d/research/eln24/NY/registration/'




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
            pause(5)
        for file in os.listdir(PATH + '/quarantine/'):
            if not os.path.exists(PATH + file):
                os.rename(PATH + '/quarantine/' + file, PATH + file)
            else:
                os.remove(PATH + '/quarantine/' + file)
    else:
        if VERBOSE:
            print(f"File already exists: {file_name}")

###############################################################################
# Setup
###############################################################################


pathlib.Path(PATH+"/quarantine/").mkdir(parents=True, exist_ok=True)

options = Options()

prefs = {
    "plugins.always_open_pdf_externally": True,  # Download PDF instead of opening in the browser
    "download.default_directory": PATH+"/quarantine/" ,  # Specify your download directory
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

while True:
    print(driver.current_url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "webny-teaser-title"))
    )

    links =[]
    links = driver.find_elements(By.XPATH, "//a[text()='Download']")


    for link in links:
        download_file_if_not_exists(link.get_attribute("href"))

    try:
        download_file_if_not_exists(driver.find_element(By.XPATH, "//a[@title='Go to next page']").get_attribute("href"))
    except NoSuchElementException:
        break
    
driver.quit()
# except:
#     print("NY registration scraper failed to retrieve stats on: " + CURR_DATE)
