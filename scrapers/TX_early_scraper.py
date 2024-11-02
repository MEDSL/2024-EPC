##############################################################################
# Script to scrape the Texas early voting data
###############################################################################
import time
from datetime import datetime
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pathlib
import csv

###############################################################################
# Global variables and setup
###############################################################################
#List the elections of interest
elections = ["2024 NOVEMBER 5TH GENERAL ELECTION"]

CURR_DATE = datetime.today().strftime("%Y%m%d")

VERBOSE = True

PATH = f"/d/research/eln24/TX/early/"
PATH_ARCHIVE = PATH + "archive_" + CURR_DATE +"/"
OTHER_PATH = '/d/research/epc_dailies/infrastructure/early/TX/raw/'

pathlib.Path(PATH_ARCHIVE).mkdir(parents=True, exist_ok=True)

options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

params = {'behavior' : 'allow', 'downloadPath' : PATH_ARCHIVE}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)


#Base texas early vote URL
BASE_URL = "https://earlyvoting.texas-election.com/Elections/getElectionEVDates.do"


###############################################################################
# Global functions
###############################################################################
#Pause for an unpredictable duration while scraping
def pause(least):
    least = max(least, 2)
    time.sleep(max(0,np.random.randint(least-1,least)+np.random.uniform(0,1)))

#Write early vote data table to directory
def saveTable(saveFileName, table, date, election):
    with open(saveFileName, "w") as f:
        f.write(table)
    if VERBOSE:
        print(f"Voting data saved for {election} on {date}")

def tryMakeDir(name, VERBOSE):
    try:
        os.makedirs(name)
    except:
        if VERBOSE:
            print(f"Writing to pre-existing folder: {name}")


###############################################################################
# Scraping loop
###############################################################################
for i in range(len(elections)):
    currElec = elections[i]

    driver.get(BASE_URL)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "idElection"))
    )

    #Populate the dropdown menu with the election of interest
    election = Select(driver.find_element(By.ID,"idElection"))
    election.select_by_visible_text(currElec)
    #Click the submit button
    driver.find_element('xpath',
            '//button[normalize-space()="Submit"]').click()

    #Get a list of the available dates
    dates = []
    dateMenu = Select(driver.find_element(By.NAME, "selectedDate"))
    dateObjs = dateMenu.options
    for j in range(len(dateObjs)):
        textDate = dateObjs[j].text
        dates.append(textDate)
    #Drop the first date, which is a header
    dates = dates[1:]

    pause(2)

    # #What dates have we already scraped for this election?
    # savedFiles = os.listdir(PATH+'quarantine/')
    # savedFiles = savedFiles + os.listdir(PATH)
    # savedFiles = [_ for _ in savedFiles if _!='quarantine']
    # doneDates = []
    # for fName in savedFiles:
    #     if currElec.replace(' ','-') in fName:
    #         dName = fName[fName.find('_')+1:]
    #         dName = dName.replace(".txt","")
    #         doneDates.append(dName)
    # datesToPull = [date for date in dates if date not in doneDates]

    # if VERBOSE and not datesToPull:
    #     print(f"Already collected all dates for {currElec}")
    # else:
    #     print(f"There are {len(datesToPull)} dates remaining to pull") 

    #Now for every date, grab the full early voting data from that date
    for date in dates:
        pause(3)

        dateMenu.select_by_visible_text(date)
        driver.find_element('xpath',
                '//button[normalize-space()="Submit"]').click()

        #Scrape the contents of the table on that page
        table = driver.find_element(By.NAME, \
                'electionsInfoForm').text

        saveFileName = PATH_ARCHIVE + currElec.replace(' ','-')+\
                       '_'+date+".txt"

        saveTable(saveFileName, table, date, currElec)

        #Return to the page that has the dates dropdown menu
        driver.execute_script("window.history.go(-1)")
        
        dateMenu = Select(driver.find_element(By.NAME, "selectedDate"))

        pause(3)

#Copy out of archive
for file in os.listdir(PATH_ARCHIVE):
    if '.html' not in file:
        file_path = PATH + file
        if not os.path.exists(file_path):
            print(f"Copied {file} from archive")
            os.system(f"cp '{PATH_ARCHIVE + file}' '{file_path}'")
    pause(2)

#Copy to the EPC Dailies directory
os.system(f"cp -r '{PATH_ARCHIVE}' '{OTHER_PATH}'")

for file in os.listdir(OTHER_PATH):
    if ('archive' not in file) and ('2020' in file):
        os.system(f"cp -r '{OTHER_PATH + file}' "+\
                  f"'{OTHER_PATH}archive_{CURR_DATE}/'")

pause(10)

driver.quit()