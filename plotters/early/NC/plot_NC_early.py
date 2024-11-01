################################################################################
# written by sbaltz at mit
################################################################################
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.patches as mpat
import statistics as stats
import numpy as np
import os
import zipfile
from makeMedslStyle import *
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm


################################################################################
# Global variables and functions
################################################################################
DATE_TO_PRINT = date.today().strftime("%m/%d/%Y")
DATE_FOR_FILE = date.today().strftime("%Y%m%d")
MAIL_NAME = A_PLACE_TO_STORE_FIGURES+f'mail_{DATE_FOR_FILE}'
EARLY_NAME = A_PLACE_TO_STORE_FIGURES+f'early_{DATE_FOR_FILE}'
CURR_DATE_MAX = datetime(year=datetime.today().year,
                         month=datetime.today().month,
                         day=datetime.today().day-1,
                         hour=12)
BASE_DIR = A_PLACE_TO_STORE_DATA_FOR_THIS_STATE
RAW_FOLDER = f'{BASE_DIR}raw/absentee_20241105_{DATE_FOR_FILE}.zip'
RAW_PREV = f'{BASE_DIR}raw/absentee_20201103.csv'
START_DAY = datetime.strptime('09/20/2024','%m/%d/%Y').date() 
CURR_DAY = datetime.today()
LAST_DAY_NOW = datetime.strptime('11/05/2024','%m/%d/%Y').date()
LAST_DAY_THEN = datetime.strptime('11/03/2020','%m/%d/%Y').date()

#If you want to go all the way to 2020 election day, True, else False
GO_TO_END = True

#Do we need to go through the whole bother of calculate the 2020 values?
PREP_2020_DATA = False

PARTIES = ['OTH', 'DEM', 'REP']
METHODS = ['MAIL', 'EARLY VOTING']

#Calculate the dates of interest in 2024
dateSeq = pd.date_range(START_DAY,CURR_DAY-timedelta(days=1),freq='d')

#Define where the label is. Allowable values:
#   'start': place it at the left side of the x-axis
#   'end': place it at the right side of the y-axis
DATE_LABEL_LOC = 'end'


################################################################################
# Read the raw data and build the dataframe to plot
################################################################################
if PREP_2020_DATA:
    prev = pd.read_csv(RAW_PREV, encoding='ISO-8859-1', low_memory=False)
    
    prev['applyDate'] = pd.to_datetime(prev.ballot_req_dt)
    prev['sendDate'] = pd.to_datetime(prev.ballot_send_dt, errors='coerce')
    prev['returnDate'] = pd.to_datetime(prev.ballot_rtn_dt, errors='coerce')
    prev.loc[(prev.voter_party_code != 'DEM') &
             (prev.voter_party_code != 'REP'), 'voter_party_code'] = 'OTH'
    prev = prev.loc[prev.ballot_rtn_status == 'ACCEPTED']
    prev.loc[prev.ballot_req_type == 'ONE-STOP', 
             'ballot_req_type'] = 'EARLY VOTING'

    #We need to generate a sequence of days that is the same number of days before
    # the 2020 election as the corresponding days are before the 2024 election. For
    # the fixed first date, it's 2 days earlier. For the moving date, it's 2 days
    # before yesterday, which is a difference of 3 days
    if GO_TO_END:
        oldEndDay = LAST_DAY_THEN
    else:
        oldEndDay = CURR_DAY - relativedelta(years=4) - timedelta(days=3)

    oldDateSeq = pd.date_range(
        pd.to_datetime(START_DAY - relativedelta(years=4) - timedelta(days=2)),
        oldEndDay,
        freq='d')
    
    #The current date sequence is simpler
    allDates = list(oldDateSeq) + list(dateSeq)
    
    #Now prepare an empty dataframe to store the plotting data
    entriesNum = len(allDates)*len(PARTIES)*len(METHODS)
    ad = pd.DataFrame(index=range(entriesNum),
                      columns = ['day','requested','sent','returned','party',
                                 'method']
                      )
    row = 0
    for party in PARTIES:
        for theDay in tqdm(list(oldDateSeq)):
            for method in METHODS:
                app = sum(prev.loc[(prev.voter_party_code == party) &
                        (prev.ballot_req_type == method),
                        'applyDate'] <= theDay)
                sen = sum(prev.loc[(prev.voter_party_code == party) &
                         (prev.ballot_req_type == method),
                         'sendDate'] <= theDay)
                ret = sum(prev.loc[(prev.voter_party_code == party) &
                                   (prev.ballot_req_type == method),
                                   'returnDate'] <= theDay)
                theRow = pd.Series([theDay,app,sen,ret,party,method])
                ad.iloc[row] = theRow
                row += 1

    ad.to_csv(f'{BASE_DIR}2020_values.csv', index=False) 
    #We're done with the 2020 dataset; drop it
    del prev
else:
    ad = pd.read_csv(f'{BASE_DIR}2020_values.csv')
    #The row to continue saving to is the first empty row
    row = min(ad.loc[ad.day.isna()].index)
    #We need enough empty rows to add all the data we have
    currEmpty = sum(ad.day.isna())
    emptyNeed = len(list(dateSeq)*len(PARTIES)*len(METHODS))
    lenDiff = emptyNeed - currEmpty
    totalLen = len(ad)
    addOn = pd.DataFrame(index = range(totalLen, totalLen+lenDiff),
                         columns = list(ad.columns)
                      )
    ad = pd.concat([ad, addOn])

#Now proceed to the 2024 file
with zipfile.ZipFile(RAW_FOLDER, 'r') as z:
    with z.open('absentee_20241105.csv') as f:
        nc = pd.read_csv(f, encoding='unicode_escape')

nc['applyDate'] = pd.to_datetime(nc.ballot_req_dt)
nc['sendDate'] = pd.to_datetime(nc.ballot_send_dt)
nc['returnDate'] = pd.to_datetime(nc.ballot_rtn_dt, errors='coerce')
nc.loc[(nc.voter_party_code != 'DEM') &
       (nc.voter_party_code != 'REP'), 'voter_party_code'] = 'OTH'

nc = nc.loc[nc.ballot_rtn_status == 'ACCEPTED']

for party in PARTIES:
    for theDay in tqdm(list(dateSeq)):
        for method in METHODS:
            app = sum(nc.loc[(nc.voter_party_code == party) &
                    (nc.ballot_req_type == method),
                    'applyDate'] <= theDay)
            sen = sum(nc.loc[(nc.voter_party_code == party) &
                     (nc.ballot_req_type == method),
                     'sendDate'] <= theDay)
            ret = sum(nc.loc[(nc.voter_party_code == party) &
                               (nc.ballot_req_type == method),
                               'returnDate'] <= theDay)
            theRow = pd.Series([theDay,app,sen,ret,party,method])
            ad.iloc[row] = theRow
            row += 1

#The x-axis will be the number of days left until the respective election
ad.day = pd.to_datetime(ad.day)
ad['daysLeft'] = pd.NA
elecDayCurr = datetime.strptime("11-05-2024", "%m-%d-%Y")
elecDayPrev = datetime.strptime("11-03-2020", "%m-%d-%Y")
ad.loc[ad.day.dt.year == 2020, 'daysLeft'] = (elecDayPrev - ad.day).dt.days
ad.loc[ad.day.dt.year == 2024, 'daysLeft'] = (elecDayCurr - ad.day).dt.days
ad['year'] = ad.day.dt.year
ad.daysLeft = ad.daysLeft.astype(int)

ad.to_csv(f'plot_data/{date.today().strftime("%Y%m%d")}.csv', index=False)


################################################################################
# Make one plot for each mode
################################################################################
for method in METHODS:
    #Figure setup
    plt.rcParams["figure.figsize"] = (10,8)
    plt.gcf().subplots_adjust(bottom=0.15,left=0.175,right=0.95)
    
    #Set the plot features that depend on the mode
    if method == 'MAIL':
        modeToPrint = 'Mail-In'
        theYLabel = "Cumulative Mail-In Ballots Accepted"
        saveFileName = MAIL_NAME
    elif method == 'EARLY VOTING':
        modeToPrint = 'Early Vote'
        theYLabel = "Cumulative Early Votes Cast"
        saveFileName = EARLY_NAME

    plt.title(f"North Carolina {modeToPrint} 2020 vs. 2024, "+\
              f"{DATE_TO_PRINT}",
              size = 21, pad = 15)
    plt.figtext(0.12,0.035,
            "Data source: North Carolina State Board of Elections, ncsbe.gov",
                size = 10)
    plt.figtext(0.12,0.015,
            "Graph source: MIT Election Data and Science Lab, @MITelectionlab",
                size = 10)
    
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.gca().yaxis.set_major_formatter(
                    mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    YMAX = max(ad.loc[ad.method == method, 'requested'])*1.1
    plt.ylim((0,YMAX))
    
    #After inspecting the data, let's restrict the plot to just begin one
    # month out
    plt.xlim((0,31))
    plt.gca().invert_xaxis()
    
    plt.ylabel(theYLabel, size = 18, labelpad = 20)
    plt.xlabel("Days Before the Election", size = 18, labelpad = 15)
    
    parties_to_cols = {
                       'DEM': medslLogoBlue,
                       'REP': medslRed,
                       'OTH': medslOrange,
                      }
    yearsToLine = {2020: 'dotted', 2024: 'solid'}
    yearsToMark = {2020: '', 2024: ''}
    
    for year in [2020, 2024]:
        curr = ad.loc[(ad.year == year) & (ad.method == method)]
        for party in PARTIES:
            plt.plot(list(curr.loc[curr.party == party, 'daysLeft']),
                     list(curr.loc[curr.party == party, 'returned']),
                     linewidth = 3,
                     color = parties_to_cols[party],
                     linestyle = yearsToLine[year],
                     marker = yearsToMark[year],
                     ms = 12,
                     alpha = 0.75)
    plt.grid(alpha=0.75)

    #Add text, and draw a line indicating what it relates to, depending on
    # the value of the global date label location variable
    if DATE_LABEL_LOC == 'start':
        labelX = 0.11
        labelY = 0.07
        plt.figtext(labelX,
                    labelY,
                    "Oct. 5 2024/\nOct. 3 2020",
                    fontsize = 12
                   )
        lineWidth = 31/1000 #0.1% of the x-axis
        plt.gca().arrow(x = 30.95,
                        y = -YMAX*0.05,
                        dx = 0,
                        dy = YMAX*0.045,
                        clip_on = False,
                        width = lineWidth,
                        color = 'black'
                        )
    elif DATE_LABEL_LOC == 'end':
        labelX = 0.89
        labelY = 0.055
        plt.figtext(labelX,
                    labelY,
                    "Nov. 5 2024/\nNov. 3 2020",
                    fontsize = 12
                   )


    legendDem = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                                  color=parties_to_cols['DEM'])
    legendRep = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                                  color=parties_to_cols['REP'])
    legendOth = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                                  color=parties_to_cols['OTH'])
    first_legend = plt.legend(loc = 'upper left', prop = {'size': 16},
        handles = [legendDem, legendRep, legendOth],
        labels = ['Democrats', 'Republicans', 'All others'],
        )

    prevEx = mpl.lines.Line2D([],[],
                              linewidth=3,
                              color='black',
                              linestyle = 'dotted',
                              markerfacecolor='black')
    currEx = mpl.lines.Line2D([],[],
                              linewidth=3,
                              color='black',
                              linestyle = 'solid',
                              markerfacecolor='black')

    second_legend = plt.legend(loc = (0.01,0.7), prop = {'size': 12},
                           handles = [prevEx, currEx],
                           handlelength = 3,
                           labels = ['2020', '2024'],
                                 )
    
    plt.gca().add_artist(first_legend)
    plt.gca().add_artist(second_legend)
    
    plt.savefig(saveFileName, dpi=400)
    plt.close()

