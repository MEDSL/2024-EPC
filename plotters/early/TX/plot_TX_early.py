###############################################################################
# written by sbaltz at mit
###############################################################################
import os
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as font_manager
from matplotlib.ticker import FuncFormatter
from datetime import date
from datetime import datetime
import sys
import copy

#Make and apply all of the medsl style requirements
BASE_DIR = A_PLACE_TO_STORE_DATA_FOR_THIS_STATE
sys.path.insert(1, A_PLACE_TO_STORE_HELPER_FILES)
from makeMedslStyle import *


###############################################################################
# Global variables
###############################################################################
#List the elections of interest
elections = ["2024-NOVEMBER-5TH-GENERAL-ELECTION",
             "2020-NOVEMBER-3RD-GENERAL-ELECTION"]

elecDates = {"2024-NOVEMBER-5TH-GENERAL-ELECTION": \
                datetime.strptime("11-05-2024", "%m-%d-%Y"),
             "2020-NOVEMBER-3RD-GENERAL-ELECTION": \
                datetime.strptime("11-03-2020", "%m-%d-%Y"),
            }

VERBOSE = True

VALIDATE = True

XSTART = 31 #Choose when the x axis begins 

os.chdir(BASE_DIR)

TODAY = datetime.strftime(datetime.today(), "%m/%d/%Y")
DATE_FOR_ARCHIVE = datetime.today().strftime("%Y%m%d")

CURR_DAYS_LEFT = (datetime.strptime("2024-11-05", "%Y-%m-%d") - \
                  datetime.today()).days + 1.5 #Don't include today

ARCHIVE_NAME = A_PLACE_TO_STORE_DATA_FOR_THIS_STATE + \
               f'archive_{DATE_FOR_ARCHIVE}/'


###############################################################################
# Data setup
###############################################################################
#The goal is to read from each file and save to a pandas dataframe
evs = pd.DataFrame(columns = ['election','daysLeft','cumulEvs'])
subEvs = pd.DataFrame(columns = ['election','daysLeft','cumulEvs'])
subIPs = pd.DataFrame(columns = ['election','daysLeft','cumulEvs'])
for election in elections:
    files = os.listdir(ARCHIVE_NAME)
    #Filer to just the current election
    files = [_ for _ in files if election in _]
    #For every date, get the table and add the cumulative early vote to a list
    allEvs = []
    subIPByDaysLeft = {}
    evsByDaysLeft = {}
    subEvsByDaysLeft = {}
    for fName in files:
        subCountyTotal = 0
        subCountyInPerson = 0

        date = fName.replace(election,"").replace(".txt","").replace(",",", ")
        date = date[1:]
        #Save the date in literal string format for checking later
        rawDate = date
        date = date.replace(",","-")
        date = date.replace('October','10-')
        date = date.replace('September','09-')
        date = date.replace('November','11-')
        date = date.replace(" ","")

        date = datetime.strptime(date, "%m-%d-%Y")
        elecDay = elecDates[election]

        daysLeft = (elecDay - date).days

        with open(ARCHIVE_NAME + fName, "r") as f:
            table = f.readlines()
        #Get the line before the table, which is signified by the date
        for l in range(len(table)):
            if rawDate in table[l]:
                startLine = l + 2
        #The table ends one line before the end, and the last line is TOTAL
        table = table[startLine:len(table)-2]
        
        countyEvs = []
        countyMail = []
        for line in table:
            #Gather cumulative early voting, so 3rd last field
            spaceLocs = [m.start() for m in re.finditer(' ',line)]
            if '2024' in fName:
                inPerson = line[spaceLocs[-7]:spaceLocs[-6]].replace("%","")
                inPerson = int(inPerson.replace(",",""))
            elif '2020' in fName:
                inPerson = line[spaceLocs[-5]:spaceLocs[-4]].replace("%","")
                inPerson = int(inPerson.replace(",",""))
            countyEvs.append(inPerson)
            if '2024' in fName:
                mailIn = line[spaceLocs[-5]:spaceLocs[-4]].replace("%","")
                mailIn = int(mailIn.replace(",",""))
            elif '2020' in fName:
                mailIn = line[spaceLocs[-3]:spaceLocs[-2]].replace("%","")
                mailIn = int(mailIn.replace(",",""))
            countyMail.append(mailIn)
        total = sum(countyEvs)
        subCountyTotal = sum(countyMail)

        #Stick it in the dictionary for that day
        evsByDaysLeft[daysLeft] = total
        subEvsByDaysLeft[daysLeft] = subCountyTotal
        subIPByDaysLeft[daysLeft] = subCountyInPerson

    #Make two lists: one of the sorted days, and one of the cumulative EVs
    daysLeft = []
    cumulEvs = []
    cumulSubEvs = []
    cumulSubIP = []
    for day in np.sort(list(evsByDaysLeft.keys())):
        daysLeft.append(day)
        cumulEvs.append(evsByDaysLeft[day])
        cumulSubEvs.append(subEvsByDaysLeft[day])
        cumulSubIP.append(subIPByDaysLeft[day])

    #Now go back and make the rows to append to the data frame
    for i in range(len(daysLeft)):
        newRow = pd.DataFrame([election,daysLeft[i],cumulEvs[i]],
                              index=evs.columns).T
        evs = pd.concat([evs, newRow], ignore_index = True)
        newSubRow = pd.DataFrame([election, daysLeft[i], cumulSubEvs[i]], \
            index = subEvs.columns).T
        subEvs = pd.concat([subEvs,newSubRow], ignore_index = True)

inPerson = copy.deepcopy(evs)
mailIn = copy.deepcopy(subEvs)

inPerson.election = inPerson.election.astype(str).str.replace('-', ' ')
mailIn.election = mailIn.election.astype(str).str.replace('-', ' ')

inPerson.to_csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE+f'inperson_{date.today().strftime("%Y%m%d")}.csv', 
           index=False) 
mailIn.to_csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE+f'mailIn_{date.today().strftime("%Y%m%d")}.csv', 
           index=False) 


###############################################################################
# Combine the two types of data into one dataframe for plotting
###############################################################################
mailIn['cat'] = 'MAIL-IN'
inPerson['cat'] = 'IN PERSON'
early = pd.concat([mailIn, inPerson])
early.reset_index(inplace=True, drop=True)
early = early.loc[early.daysLeft >= CURR_DAYS_LEFT]


###############################################################################
# Plot 2024 vs 2020 mail-in and in-person early
###############################################################################
YMAX = max(early.cumulEvs)

plt.rcParams["figure.figsize"] = (11.9,10)
plt.gcf().subplots_adjust(bottom=0.15,left=0.15,right=0.95)

early.daysLeft = early.daysLeft.astype(int)
plt.xticks(range(int(np.ceil(CURR_DAYS_LEFT)),max(early.daysLeft),5))
plt.xticks(fontsize=15)

#Set the y-axis in millions
def millions(x, pos):
    if x == 0:
        val = x
    else:
        val = '%1.1fM' % (x * 1e-6)
    return(val)

formatter = FuncFormatter(millions)
plt.yticks(range(0,int(max(early.cumulEvs)*1.1),500000))
plt.yticks(fontsize=15)

plt.gca().yaxis.set_major_formatter(formatter)

plt.xlim(CURR_DAYS_LEFT,XSTART)
plt.ylim(-50000,YMAX*1.1)

yearsToLine = {'2020': 'dotted', '2024': 'solid'}
catToCol = {'MAIL-IN': medslDarkGreen,
            'IN PERSON': medslLightPurple
            }
yearsToMark = {'2020': 'o', '2024': 's'}

orderedElecs = ["2020 NOVEMBER 3RD GENERAL ELECTION",
                "2024 NOVEMBER 5TH GENERAL ELECTION"]
for elec in orderedElecs:
    if '2020' in elec:
        year = '2020'
    elif '2024' in elec:
        year = '2024'
    for cat in ['MAIL-IN', 'IN PERSON']:
        curr = early.loc[(early.election == elec) & (early.cat == cat)]
        plt.plot(curr.daysLeft, curr.cumulEvs,
                 linewidth = 3,
                 color = catToCol[cat],
                 ms = 12,
                 marker = yearsToMark[year],
                 linestyle = yearsToLine[year],
                 alpha = 0.9
                )
plt.grid(alpha=0.75)
plt.legend(prop={'size': 14}, loc="upper left")
plt.gca().invert_xaxis()
#plt.vlines(x=30, linestyles='dashed', colors=medslChartGrey, alpha=0.5,
#           ymin = 0, ymax = YMAX*2, linewidth=5)
#plt.text(x = 31.9, y = 1/2*YMAX, s=" Start of \n 2020 data \n reporting",
#         size = 'x-large', backgroundcolor='white')
plt.figtext(0.05,0.03,"Data source: Texas Secretary of State, https://earlyvoting.texas-election.com")
plt.figtext(0.6,0.03,"Note: in-person early voting began earlier in 2020 than in 2024.")
plt.figtext(0.6,0.01,"In the y-axis, M stands for million.")
#Graph source
plt.figtext(0.05,0.01,"Graph source: MIT Election Data and Science Lab, @MITelectionlab")
plt.ylabel("Cumulative Number of Early Voters",
                  size = 18, labelpad = 20)
plt.xlabel("Days Before the Election", size = 18, labelpad = 20)
plt.title(f"Texas Early Votes 2020 vs 2024, {TODAY}",
                 size = 26, pad = 20)
#Add text, and draw a line indicating what it relates to
labelX = 0.11
labelY = 0.075
plt.figtext(labelX,
            labelY,
            "Oct. 5 2024/\nOct. 3 2020",
            fontsize = 12
           )
lineWidth = (max(early.daysLeft)-CURR_DAYS_LEFT)/1000 #0.1% of the x-axis
plt.gca().arrow(x = 30.95,
                y = -300000,
                dx = 0,
                dy = 225000,
                clip_on = False,
                width = lineWidth,
                color = 'black'
                )
prevMail = mpl.lines.Line2D([],[],linewidth=5,
                            color = catToCol['MAIL-IN'],
                            marker = yearsToMark['2020'],
                            ms = 14,
                            linestyle = 'dotted')
currMail = mpl.lines.Line2D([],[],linewidth=5,
                            color = catToCol['MAIL-IN'],
                            marker = yearsToMark['2024'],
                            ms = 14,
                            linestyle = yearsToLine['2024'])
prevEarly = mpl.lines.Line2D([],[],linewidth=5,
                             color = catToCol['IN PERSON'],
                             marker = yearsToMark['2020'],
                             ms = 14,
                             linestyle = 'dotted')
currEarly = mpl.lines.Line2D([],[],linewidth=5,
                             color = catToCol['IN PERSON'],
                             marker = yearsToMark['2024'],
                             ms = 14,
                             linestyle = yearsToLine['2024'])
plt.legend(loc = "upper left",
           prop = {'size': 16},
           handles = [prevMail,currMail,prevEarly,currEarly],
           handlelength = 3,
           labels = ['Mail-In Ballots Returned 2020',
                     'Mail-In Ballots Returned 2024',
                     'In-Person Early Votes 2020',
                     'In-Person Early Votes 2024'
                    ],
          )
plt.savefig(A_PLACE_TO_STORE_FIGURES +\
            date.today().strftime("%Y%m%d") + ".png")

