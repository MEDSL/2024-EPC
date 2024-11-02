###############################################################################
# Script to scrape Oregon voter registration data
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
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://sos.oregon.gov/elections/Pages/electionsstatistics.aspx"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/OR/registration/"
PATH = '/d/research/eln24/OR/registration/'



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

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "accordion-toggle"))
    )

    dropdowns = driver.find_elements(By.CLASS_NAME, "accordion-toggle")

    saved_hrefs = []
    monthly_hrefs = []

    # Click each dropdown and collect the links
    for dropdown in dropdowns:
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        pause(2)
        driver.execute_script("arguments[0].click();", dropdown)
        
        # Extract the year from the href attribute of the dropdown
        year = dropdown.get_attribute('href').split('#')[-1]

        pause(3)
        # Collect links that contain the specific year in their partial link text
        year_links = driver.find_elements(By.PARTIAL_LINK_TEXT, " "+str(year))
        for year_link in year_links:
            href = year_link.get_attribute("href")
            if ".pdf" in href:
                download_file_if_not_exists(href)
            else:
                monthly_hrefs.append(href)
        
    for year in range(2001, 2018 + 1):
        year_links = driver.find_elements(By.PARTIAL_LINK_TEXT, str(year))
        for year_link in year_links:
            href = year_link.get_attribute("href")
            saved_hrefs.append(href)

    # Process saved hrefs
    for href in saved_hrefs:
        driver.get(href)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Voter Registration"))
        )

        voter_registration_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Voter Registration")
        for vr_link in voter_registration_links:
            monthly_hrefs.append(vr_link.get_attribute("href"))

    for page in monthly_hrefs:
        driver.get(page)
        view_download_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn.dropdown-toggle"))
        )
        view_download_button.click()
        pause(1)
        download = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download"))
        )
        download.click()    

except Exception as e:
    print(f"OR registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()
