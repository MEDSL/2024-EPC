###############################################################################
# Script to scrape Washington voter registration data
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
import pyperclip
import pyautogui



###############################################################################
# Global variables
###############################################################################
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://sosmt.gov/elections/regvotercounty/"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/MT/registration/"
PATH = '/d/research/eln24/MT/registration/'



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


pathlib.Path(PATH +'quarantine/').mkdir(parents=True, exist_ok=True)

options = Options()

prefs = {
    "plugins.always_open_pdf_externally": True,  # Download PDF instead of opening in the browser
    "download.default_directory": PATH + 'quarantine/',  # Specify your download directory
    "download.prompt_for_download": False,  # Disable the download prompt
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--window-size=2560,1440")
os.remove(ChromeDriverManager().install())

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


###############################################################################
# Scrape
###############################################################################

try:
    driver.get(BASE_URL)

    
    pause(5)

    pyautogui.moveTo(300, 720, duration=1)
    pyautogui.scroll(-10)
    pause(20)
    pyautogui.moveTo(1300, 850, duration=1)
    pyautogui.leftClick()
    pause(5)
    pyautogui.moveTo(1000, 650, duration=1)
    pyautogui.leftClick()

    pause(5)
    os.rename(PATH + '/quarantine/County Data.xlsx', PATH + CURR_DATE+'.xlsx')

    pause(5)






except Exception as e:
    print(f"MT registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()
