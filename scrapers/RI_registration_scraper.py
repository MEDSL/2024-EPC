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
date_strings = [
    'aug_2024', 'jul_2024', 'jun_2024', 'may_2024', 'apr_2024', 'mar_2024', 'feb_2024', 'jan_2024',
    'dec_2023', 'nov_2023', 'oct_2023', 'sep_2023', 'aug_2023', 'jul_2023', 'jun_2023', 'may_2023',
    'apr_2023', 'mar_2023', 'feb_2023', 'jan_2023', 'dec_2022', 'nov_2022', 'oct_2022', 'sep_2022',
    'aug_2022', 'jul_2022', 'jun_2022', 'may_2022', 'apr_2022', 'mar_2022', 'feb_2022', 'jan_2022',
    'dec_2021', 'nov_2021', 'oct_2021', 'sep_2021', 'aug_2021', 'jul_2021', 'jun_2021', 'may_2021',
    'apr_2021', 'mar_2021', 'feb_2021', 'jan_2021', 'dec_2020', 'nov_2020', 'oct_2020', 'sep_2020',
    'aug_2020', 'jul_2020', 'jun_2020', 'may_2020', 'apr_2020', 'mar_2020', 'feb_2020', 'jan_2020',
    'dec_2019', 'nov_2019', 'oct_2019', 'sep_2019', 'aug_2019', 'jul_2019', 'jun_2019', 'may_2019',
    'apr_2019', 'mar_2019', 'feb_2019', 'jan_2019', 'dec_2018', 'nov_2018', 'oct_2018', 'sep_2018',
    'aug_2018', 'jul_2018'
]

VERBOSE = False

CURR_DATE = datetime.today().strftime("%Y%m%d")

BASE_URL = "https://datahub.sos.ri.gov/RegisteredVoter.aspx"

# PATH = "/Users/sinashaikh/Desktop/MEDSL/RI/registration/"
PATH = '/d/research/eln24/RI/registration/'



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
options.add_argument("--window-size=2560,1440")
os.remove(ChromeDriverManager().install())

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


###############################################################################
# Scrape
###############################################################################


driver.get(BASE_URL)
pause(5)


try:

    pyautogui.moveTo(680, 650, duration=1)
    pyautogui.leftClick()
    pyautogui.rightClick()
    pyautogui.moveTo(900, 660, duration=1)
    pyautogui.moveTo(900, 690, duration=1)

    pyautogui.leftClick()

    s = pyperclip.paste() 
    with open(PATH+CURR_DATE+'dem.txt','w') as g:
        g.write(s)


    pyautogui.moveTo(900, 650, duration=1)
    pyautogui.leftClick()
    pyautogui.rightClick()
    pyautogui.moveTo(1120, 660, duration=1)
    pyautogui.moveTo(1120, 690, duration=1)

    pyautogui.leftClick()

    s = pyperclip.paste() 
    with open(PATH+CURR_DATE+'no_lab.txt','w') as g:
        g.write(s)

    pyautogui.moveTo(1100, 650, duration=1)
    pyautogui.leftClick()
    pyautogui.rightClick()
    pyautogui.moveTo(1320, 660, duration=1)
    pyautogui.moveTo(1320, 690, duration=1)

    pyautogui.leftClick()

    s = pyperclip.paste() 

    with open(PATH+CURR_DATE+'rep.txt','w') as g:
        g.write(s)


    pyautogui.moveTo(1300, 650, duration=1)
    pyautogui.leftClick()
    pyautogui.rightClick()
    pyautogui.moveTo(1520, 660, duration=1)
    pyautogui.moveTo(1520, 690, duration=1)

    pyautogui.leftClick()

    s = pyperclip.paste() 
    with open(PATH+CURR_DATE+'unaff.txt','w') as g:
        g.write(s)





    #### Note: this is for getting past data
    # for date in date_strings[27:]:
    #     pyautogui.moveTo(680, 650, duration=1)
    #     pyautogui.leftClick()
    #     pyautogui.rightClick()
    #     pyautogui.moveTo(900, 660, duration=1)
    #     pyautogui.moveTo(900, 690, duration=1)

    #     pyautogui.leftClick()

    #     s = pyperclip.paste() 
    #     with open(PATH+date+'dem.txt','w') as g:
    #         g.write(s)


    #     pyautogui.moveTo(900, 650, duration=1)
    #     pyautogui.leftClick()
    #     pyautogui.rightClick()
    #     pyautogui.moveTo(1120, 660, duration=1)
    #     pyautogui.moveTo(1120, 690, duration=1)

    #     pyautogui.leftClick()

    #     s = pyperclip.paste() 
    #     if date in [ 'aug_2024', 'jul_2024']:
    #         with open(PATH+date+'no_lab.txt','w') as g:
    #             g.write(s)
    #     else:
    #         with open(PATH+date+'rep.txt','w') as g:
    #             g.write(s)

    #     pyautogui.moveTo(1100, 650, duration=1)
    #     pyautogui.leftClick()
    #     pyautogui.rightClick()
    #     pyautogui.moveTo(1320, 660, duration=1)
    #     pyautogui.moveTo(1320, 690, duration=1)

    #     pyautogui.leftClick()

    #     s = pyperclip.paste() 
    #     if date in [ 'aug_2024', 'jul_2024']:
    #         with open(PATH+date+'rep.txt','w') as g:
    #             g.write(s)
    #     else:
    #         with open(PATH+date+'unaff.txt','w') as g:
    #             g.write(s)

    #     pyautogui.moveTo(1300, 650, duration=1)
    #     pyautogui.leftClick()
    #     pyautogui.rightClick()
    #     pyautogui.moveTo(1520, 660, duration=1)
    #     pyautogui.moveTo(1520, 690, duration=1)

    #     pyautogui.leftClick()

    #     s = pyperclip.paste() 
    #     if date in [ 'aug_2024', 'jul_2024']:
    #         with open(PATH+date+'unaff.txt','w') as g:
    #             g.write(s)


    #     pyautogui.moveTo(1500, 350, duration=1)
    #     pyautogui.leftClick()
    #     pyautogui.moveTo(1500, 382 + (date_strings.index(date)+1), duration=1)
    #     pause(2)
    #     pyautogui.scroll(-1*((date_strings.index(date)+1)/2))

    #     if (date_strings.index(date)+1) % 2:
    #         pyautogui.moveTo(1500, 408 + (date_strings.index(date)+1), duration=1)
    #     pause(2)
    #     pyautogui.leftClick()
    #     pause(10)




except Exception as e:
    print(f"WA registration scraper failed to retrieve stats on {CURR_DATE}: {str(e)}")

finally:
    driver.quit()
