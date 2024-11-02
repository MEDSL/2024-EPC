import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.patches as mpat
import statistics as stats
import numpy as np
import os
import sys
from datetime import date
from datetime import datetime

BASE_DIR = A_PLACE_TO_STORE_DATA_FOR_THIS_STATE
sys.path.insert(1, A_PLACE_TO_STORE_HELPER_FILES)
from makeMedslStyle import *


################################################################################
# Global variables and functions
################################################################################
DATE_TO_PRINT = date.today().strftime("%m/%d/%Y")
FIG_NAME = A_PLACE_TO_STORE_FIGURES+\
           date.today().strftime("%Y%m%d")
#Set the x axis to end tomorrow, to make room for labels
CURR_DATE_MAX = datetime(year=datetime.today().year,
                         month=datetime.today().month,
                         day=datetime.today().day + 2,
                         hour=12)

def BuildDf(fnames):
    ad = pd.DataFrame(index = range(len(fnames)),
                      columns = ['day','cat','dem','rep','npa','oth']
                     )
    for i in range(len(fnames)):
        fname = fnames[i]
        curr = pd.read_csv(fname, sep="\t")
        dateLoc = fname.find(f'{BASE_DIR}raw/files/') + \
                             len(f'{BASE_DIR}raw/files/')
        dateStr = fname[dateLoc:dateLoc+8]
        ad.iloc[i].day = datetime.strptime(dateStr,'%Y%m%d').date()
        if 'provided' in fname:
            ad.iloc[i]['cat'] = 'provided'
        elif 'voted' in fname:
            ad.iloc[i]['cat'] = 'voted'
        elif 'early' in fname:
            ad.iloc[i]['cat'] = 'early'
        ad.iloc[i].dem = curr.loc[curr.CountyName=='State Totals', 'TotalDem'][0]
        ad.iloc[i].rep = curr.loc[curr.CountyName=='State Totals', 'TotalRep'][0]
        ad.iloc[i].npa = curr.loc[curr.CountyName=='State Totals', 'TotalNpa'][0]
        ad.iloc[i].oth = curr.loc[curr.CountyName=='State Totals', 'TotalOth'][0]
         
    return(ad)
     

################################################################################
# Generate data
################################################################################
fnames = os.listdir(f'{BASE_DIR}raw/files/')
fnames = [f'{BASE_DIR}raw/files/' + _ for _ in fnames]

early = BuildDf(fnames)

#There is one more date that can be constructed manually using data available
# on the web archive. We do this part manually since it is unchanging
preDf = pd.DataFrame(index = range(2),
                      columns = ['day','cat','dem','rep','npa','oth']
                     )
preDf.iloc[0] = ['2024-09-12', 'provided', '1524', '2139', '1073', '120']
preDf.iloc[1] = ['2024-09-12', 'voted', '0', '1', '0', '1']

early = pd.concat([early, preDf])
early.reset_index(inplace=True, drop=True)

early.day = pd.to_datetime(early.day, format='%Y-%m-%d')
early = early.sort_values(by='day')

#Subset to dates before the current day
early = early.loc[early.day < pd.to_datetime(datetime.today().date())]


################################################################################
# Plot
################################################################################
plt.rcParams["figure.figsize"] = (11.9,10)
plt.gcf().subplots_adjust(bottom=0.15,left=0.175,right=0.95)
plt.title(f'Florida Mail Ballot Status, {DATE_TO_PRINT}',
          size = 25, pad = 15)
plt.figtext(0.025,0.04,
"For each party, a label shows the percent of ballots issued to members of "+\
"that party that have been returned.",
            size = 12)
plt.figtext(0.025,0.015,
"Data from Florida Division of Elections, countyballotfiles.floridados.gov"+\
". Graph from MIT Election Data and Science Lab, @MITelectionlab.",
            size = 12)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
format_date = mpl.dates.DateFormatter('%b %d')
plt.gca().xaxis.set_major_formatter(format_date)
plt.gca().xaxis.set_major_locator(mpl.dates.DayLocator(interval=7))
plt.xlim((datetime(year=2024,month=9,day=11,hour=12),
          CURR_DATE_MAX
          ))
plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylabel("Cumulative Number of Mail Ballots", size = 18, labelpad = 20)
plt.xlabel("Status as of", size = 18, labelpad = 25)

#The number *sent* is the number *provided but not voted* (which the state calls
# "provided") plus the number voted already
for party in ['dem', 'rep', 'npa', 'oth']:
    early[party] = early[party].astype(str).str.replace(',','').astype(int)
for day in pd.unique(early.day):
    for party in ['dem', 'rep', 'npa', 'oth']:
        voted = int(early.loc[(early.day == day) & (early['cat'] == 'voted'), party])
        early.loc[(early.day == day) & \
                  (early['cat'] == 'provided'), party] += voted
provided = early.loc[early['cat'] == 'provided']
voted = early.loc[early['cat'] == 'voted']
ip = early.loc[early['cat'] == 'early']

provided.reset_index(inplace=True, drop=True)
voted.reset_index(inplace=True, drop=True)
ip.reset_index(inplace=True, drop=True)

vars_to_cols = {
                'dem': medslLogoBlue,
                'rep': medslRed,
                'npa': medslLightPurple,
                'oth': medslGold
                }
plt.grid(alpha=0.75)

provided.to_csv(f'plot_data/{date.today().strftime("%Y%m%d")}_provided.csv',
                index=False)
voted.to_csv(f'plot_data/{date.today().strftime("%Y%m%d")}_voted.csv',
             index=False)

for var in vars_to_cols.keys():
    for party in vars_to_cols.keys():
        plt.plot_date(list(provided['day']), list(provided[party]),
                      linewidth=3, color = vars_to_cols[party],
                      ms = 8,marker='o',
                      linestyle = 'dotted', alpha=0.5)
        plt.plot_date(list(voted['day']), list(voted[party]),
                      ms=8,marker='s',
                      color = vars_to_cols[party],
                      linestyle='solid', linewidth=3, alpha=0.5
                      )

#Add text to the points. First draw blank points for today and tomorrow, to
#make extra space on the plot
lab_locs = {}
lab_vals = {}
xLabLoc = datetime(year=datetime.today().year,
                   month=datetime.today().month,
                   day=datetime.today().day - 1,
                   hour=20)
yesterday = datetime(year=datetime.today().year,
                     month=datetime.today().month,
                     day=datetime.today().day - 1)
ymax = provided[['dem','rep','npa','oth']].max().max()
for party in ['dem','rep','npa','oth']:
    #Reduce height by some amount to make it line up with the points
    yLabLoc = voted.loc[voted.day == yesterday, party]
    yLabLoc -= 0.0075*ymax
    lab_locs[party] = (xLabLoc, yLabLoc)
    issued = provided.loc[provided.day == yesterday, party].item()
    returned = voted.loc[voted.day == yesterday, party].item()
    pct = returned / issued
    pct *= 100
    lab_vals[party] = int(round(pct, 0))
#Now add the text
for party in ['dem','rep','npa','oth']:
    plt.text(x = lab_locs[party][0],
             y = lab_locs[party][1],
             s = f'{lab_vals[party]}%',
             fontsize = 12,
             backgroundcolor = 'white'
             )


legendDem = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                              color=vars_to_cols['dem'],
                              markerfacecolor=vars_to_cols['dem'])
legendRep = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                                 color=vars_to_cols['rep'],
                                 markerfacecolor=vars_to_cols['rep'])
legendNpa = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                                 color=vars_to_cols['npa'],
                                 markerfacecolor=vars_to_cols['npa'])
legendOth = mpl.lines.Line2D([],[],linewidth=5,ms=10,
                                 color=vars_to_cols['oth'],
                                 markerfacecolor=vars_to_cols['oth'])
proviEx = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color='black',
                                 linestyle = 'dotted',
                                 markerfacecolor='black')
votedEx = mpl.lines.Line2D([],[],marker='s',
                                 linewidth=5,ms=10,
                                 color='black',
                                 linestyle = 'solid',
                                 markerfacecolor='black')
first_legend = plt.legend(loc = (0.01,0.8), prop = {'size': 12},
    handles = [legendDem, legendRep, legendNpa, legendOth],
    handlelength = 3,
    labels = ['Democrat', 'Republican      ', 'No Party', 'Other'],
          )
second_legend = plt.legend(loc = (0.01,0.7), prop = {'size': 12},
                           handles = [proviEx, votedEx],
                           handlelength = 3,
                           labels = ['Mail Issued', 'Mail Returned'],
                                 )
plt.gca().add_artist(first_legend)
plt.gca().add_artist(second_legend)
plt.savefig(FIG_NAME, dpi=400)
plt.close()


