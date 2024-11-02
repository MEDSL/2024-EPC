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
import csv

###############################################################################
# Global variables
###############################################################################
VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://elections.wi.gov/statistics-data/absentee-statistics"

# PATH = '/Users/sinashaikh/Desktop/MEDSL/WI/early/'
PATH = '/d/research/eln24/WI/early/'

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

def moveLatest(new_name):
    for file in os.listdir(PATH + 'quarantine/'):
        if not file.__contains__('.html'):
            file_path = PATH + new_name + '.' + file.split('.', 1)[1]
            if not os.path.exists(file_path):
                print(file_path)
                os.rename(PATH + 'quarantine/' + file, file_path)
        pause(2)


def download_file_if_not_exists(url):
    file_name = url.split("/")[-1]
    file_path = os.path.join(PATH, file_name).replace("%", " ")
    print(file_path)
    if not os.path.exists(file_path):
        driver.get(url)
        pause(5)
    else:
        if VERBOSE:
            print(f"File already exists: {file_name}")



###############################################################################
# Setup
###############################################################################

pathlib.Path(PATH + "quarantine/").mkdir(parents=True, exist_ok=True)

options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

params = {'behavior' : 'allow', 'downloadPath' : PATH + "quarantine/"}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

###############################################################################
# Scrape
###############################################################################



driver.get(BASE_URL)

while True:

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "views-row"))
    )

    links =[]
    # links = driver.find_elements(By.PARTIAL_LINK_TEXT, "2020 General Election")
    links = links + (driver.find_elements(By.PARTIAL_LINK_TEXT, "2024 General Election"))
                 
    for link in links:
        print(link.text)
        link.click()
        date_updated = driver.find_element(By.TAG_NAME, 'time').get_attribute('datetime')[:10]
        if driver.find_elements(By.PARTIAL_LINK_TEXT, "Muni"):
            days = driver.find_elements(By.PARTIAL_LINK_TEXT, "Muni")
            for day in days:
                print(day.text)
                os.system('rm -rf {PATH}quarantine/*')
                print(PATH+date_updated+".csv")
                if not os.path.exists(PATH+date_updated+".csv") and not os.path.exists(PATH+date_updated+".xlsx") and not os.path.exists(PATH+day.text+".csv"):
                    print("hello")
                    driver.get(day.get_attribute("href"))
                    pause(3)
                    if(len(days) > 1 or "2024" in date_updated):
                        moveLatest(day.text)
                    else:
                        print("2020 running")
                        moveLatest(date_updated)
        else:
            table = driver.find_element(By.TAG_NAME, 'table')

            table_data = []

            headers = [header.text.strip() for header in table.find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')]
            table_data.append(headers)


            rows = table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text.strip() for cell in cells]
                if row_data:
                    table_data.append(row_data)


            with open(PATH + f'{date_updated}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(table_data)

        driver.back()
        pause(15)

    try:
        driver.get(driver.find_element(By.XPATH, "//a[@title='Go to next page']").get_attribute("href"))
    except NoSuchElementException:
        break

# Copy over to other folder for EPC dailies
OTHER_PATH = '/d/research/epc_dailies/infrastructure/early/WI/raw/'

for file_name in os.listdir(PATH):
    if not os.path.exists(OTHER_PATH + file_name):
        os.system(f"cp '{PATH + file_name}' '{OTHER_PATH}'")

pause(10)


