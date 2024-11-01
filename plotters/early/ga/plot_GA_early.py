#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:28:41 2024

@authors: zdjgarai, Sina Shaikh

Georgia Early and Absentee Voting Script
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.patches as mpat
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import statistics as stats
import numpy as np
import os
from makeMedslStyle import *
from datetime import date, timedelta
from datetime import datetime
from matplotlib.ticker import FuncFormatter


################################################################################
# Global variables and functions
################################################################################
DATE_TO_PRINT = date.today().strftime("%m/%d/%Y")
FIG_NAME = A_PLACE_TO_STORE_FIGURES+\
           date.today().strftime("%Y%m%d")


CURR_DATE_MAX = datetime(year=datetime.today().year,
                         month=datetime.today().month,
                         day=datetime.today().day,
                         hour=12)

medslLightPurple = "#948de5"
medslDarkGreen = "#37C256"
medslChartGrey = "#c4c4c4"
medslDarkOrange = "#D46200"
medslGold = "#c0ba79"

CURR_DAYS_LEFT = (datetime.strptime("2024-11-05", "%Y-%m-%d") - \
                  datetime.today()).days + 1.5 #Don't include today



################################################################################
# Read and process 2024 data
################################################################################

GAdf = pd.DataFrame(columns=['day', 'county_name', 'accepted', 'outstanding', 'rejected', 'cancelled', 'spoiled', 'sent', 'returned', 'acc_abs', 'acc_early'])
j = 0

os.chdir(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE) 
elapsed = (date.today() - date(2024, 8, 19)).days
dates = pd.date_range(datetime.strptime('8/19/2024', '%m/%d/%Y'), periods=elapsed)

GAr = pd.read_csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE + str(date.today().strftime("%-m/%-d/%y")).replace('/', '-') + '/STATEWIDE.csv') # reading in statewide data for plot day
GAr = GAr[GAr['Ballot Issued Date'].apply(lambda x: str(x)) != 'nan'] # eliminate NA issue dates
GAr = GAr[GAr['Ballot Issued Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y')) >= datetime.strptime('8/19/2024', '%m/%d/%Y')]
GAr = GAr[GAr['Ballot Issued Date'] <= dates[-1].strftime("%m/%d/%Y")]


for plot_day in dates:
    GApd = GAr[GAr['Ballot Issued Date'] <= plot_day.strftime("%m/%d/%Y")]
    GArd = GAr[GAr['Ballot Return Date'] <= plot_day.strftime("%m/%d/%Y")]

    
    Ac = GArd[GArd['Ballot Status'] == 'A'].shape[0]
    Ic = GArd[GArd['Ballot Status'] == 'I'].shape[0]
    Rc = GArd[GArd['Ballot Status'] == 'R'].shape[0]
    Cc = GApd[GApd['Ballot Status'] == 'C'].shape[0]
    Sc = GArd[GArd['Ballot Status'] == 'S'].shape[0]
    Tc = GApd['Ballot Status'].shape[0] - Cc # subtract cancelled
    Vc = Ac + Rc + Sc # returned
    Øc = Tc - Ac - Ic - Rc - Sc
    
    Accepted = GArd[GArd['Ballot Status'] == 'A']
    
    IMc = GApd[GApd['Ballot Style'] != 'EARLY IN-PERSON']['Ballot Status'].shape[0]
    AEc = Accepted[Accepted['Ballot Style'] == 'EARLY IN-PERSON'].shape[0] # early in-person
    AMc = Accepted[Accepted['Ballot Style'] != 'EARLY IN-PERSON'].shape[0] # mailed in successfully

    
    GAdf.loc[j] = [plot_day, 'STATEWIDE', Ac, Ic, Rc, Cc, Sc, IMc, Vc, AMc, AEc]
    j = j + 1


GAdf.to_csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE + str(date.today().strftime("%m/%d/%Y")).replace('/', '-') + '.csv') 


early = GAdf[GAdf['county_name'] == 'STATEWIDE'] # uses the statewide data to generate the plot
GA_absentee = GAdf[GAdf['county_name'] != 'STATEWIDE'] 

################################################################################
# Read and process 2020 data
################################################################################


GAdf_2020 = pd.DataFrame(columns=['day', 'county_name', 'accepted', 'outstanding', 'rejected', 'cancelled', 'spoiled', 'sent', 'returned', 'acc_abs', 'acc_early'])
j = 0

os.chdir(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE) 
elapsed = ((date.today() - timedelta(days=1)).replace(year=2020) - date(2020, 8, 19)).days
dates = pd.date_range(datetime.strptime('8/19/2020', '%m/%d/%Y'), periods=elapsed)

GAr = pd.read_csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE+r'20201103_STATEWIDE.csv') # reading in statewide data for 2020

GAr = GAr[GAr['Ballot Issued Date'].apply(lambda x: str(x)) != 'nan'] # eliminate NA issue dates
GAr = GAr[GAr['Ballot Issued Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y')) >= datetime.strptime('8/19/2020', '%m/%d/%Y')]
GAr = GAr[GAr['Ballot Issued Date'] <= dates[-1].strftime("%m/%d/%Y")]


for plot_day in dates:
    GApd = GAr[GAr['Ballot Issued Date'] <= plot_day.strftime("%m/%d/%Y")]
    GArd = GAr[GAr['Ballot Return Date'] <= plot_day.strftime("%m/%d/%Y")]

    
    Ac = GArd[GArd['Ballot Status'] == 'A'].shape[0]
    Ic = GArd[GArd['Ballot Status'] == 'I'].shape[0]
    Rc = GArd[GArd['Ballot Status'] == 'R'].shape[0]
    Cc = GApd[GApd['Ballot Status'] == 'C'].shape[0]
    Sc = GArd[GArd['Ballot Status'] == 'S'].shape[0]
    Tc = GApd['Ballot Status'].shape[0] - Cc # subtract cancelled
    Vc = Ac + Rc + Sc # returned
    Øc = Tc - Ac - Ic - Rc - Sc
    
    Accepted = GArd[GArd['Ballot Status'] == 'A']
    
    IMc = GApd[GApd['Ballot Style'] != 'IN PERSON']['Ballot Status'].shape[0]
    AEc = Accepted[Accepted['Ballot Style'] == 'IN PERSON'].shape[0] # early in-person
    AMc = Accepted[Accepted['Ballot Style'] != 'IN PERSON'].shape[0] # mailed in successfully

    
    GAdf_2020.loc[j] = [plot_day, 'STATEWIDE', Ac, Ic, Rc, Cc, Sc, IMc, Vc, AMc, AEc]
    j = j + 1

GAdf_2020.to_csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE+r'pd_2020.csv') 


early_2020 = GAdf_2020[GAdf_2020['county_name'] == 'STATEWIDE'] # uses the statewide data to generate the plot


early['day'] = pd.to_datetime(early['day'])
early = early.sort_values(by='day')

early_2020['day'] = pd.to_datetime(early_2020['day'])
early_2020 = early_2020.sort_values(by='day')


early_2020['day'] = pd.to_datetime(early_2020['day'].dt.strftime("2024-%m-%d")) + pd.DateOffset(days=2)
early_2020 = early_2020.sort_values(by='day')

print(early)
print(early_2020)


early['day'] = (datetime.strptime("11-05-2024", "%m-%d-%Y") - early['day']).dt.days
early_2020['day'] = (datetime.strptime("11-05-2024", "%m-%d-%Y") - early_2020['day']).dt.days

print(early)
print(early_2020)

################################################################################
# Plot
################################################################################
plt.rcParams["figure.figsize"] = (10,8)
ax = plt.axes()
ax.set_facecolor('white')

plt.figtext(.095,
            .065,
            "Sep. 16 2024/\nSep. 14 2020",
            fontsize = 12
           )

plt.gcf().subplots_adjust(bottom=0.15,left=0.15,right=0.95)
plt.title(f'Georgia Early Vote Status, {DATE_TO_PRINT}',
          size = 25, pad = 15)
plt.figtext(0.05,0.03,"Data source: Georgia Secretary of State, sos.ga.gov")
plt.figtext(0.05,0.01,"Graph source: MIT Election Data and Science Lab, @MITelectionlab")


def millions(x, pos):
    if x == 0:
        val = x
    else:
        val = '%1.1fM' % (x * 1e-6)
    return(val)

formatter = FuncFormatter(millions)
plt.yticks(ticks = range(0,max(max(early.sent), max(early.acc_early), max(early_2020.sent), max(early_2020.acc_early)),500000), fontsize=15)
plt.gca().yaxis.set_major_formatter(formatter)


plt.xticks(fontsize=15)
# format_date = mpl.dates.DateFormatter('%b %d')
# plt.gca().xaxis.set_major_formatter(format_date)
# plt.gca().xaxis.set_major_locator(mpl.dates.WeekdayLocator(byweekday=MO))

plt.xlim(CURR_DAYS_LEFT - 3, 50)
plt.ylim((-10000,max(max(early.sent), max(early.acc_early), max(early_2020.sent), max(early_2020.acc_early))*1.1))
plt.ylabel("Number of Ballots", size = 18, labelpad = 20)
#plt.xlabel("Processing Date", size = 18, labelpad = 7.5)
plt.xlabel("Days Before the Election", size = 18, labelpad = 7.5)
vars_to_cols = {
                'sent': medslGold,
                'acc_abs': medslDarkGreen,
                'acc_early': medslLightPurple
                }
plt.grid(color=medslChartGrey, alpha=0.75)

plt.gca().invert_xaxis()



for var in vars_to_cols.keys():
    plt.plot(list(early['day']), list(early[var]),
                  linewidth=5, color = vars_to_cols[var], marker = '')
    plt.plot(list(early_2020['day']), list(early_2020[var]),
                  linewidth=5, color = vars_to_cols[var], marker = '', ls = 'dotted')

plt.text(x = CURR_DAYS_LEFT,
             y = early_2020['acc_abs'].iloc[-1],
             s = f"{early_2020['acc_abs'].iloc[-1] / early_2020['sent'].iloc[-1]:.0%}",
             fontsize = 12,
             backgroundcolor = 'white',
             verticalalignment ='center_baseline'
             )

plt.text(x = CURR_DAYS_LEFT,
             y = early['acc_abs'].iloc[-1],
             s = f"{early['acc_abs'].iloc[-1] / early['sent'].iloc[-1]:.0%}",
             fontsize = 12,
             backgroundcolor = 'white',
             verticalalignment ='center_baseline'
             )

legendSent = mpl.lines.Line2D([],[],marker='',linewidth=5,
                              color=vars_to_cols['sent'],
                              markerfacecolor=vars_to_cols['sent'])
legendReturned = mpl.lines.Line2D([],[],marker='',linewidth=5,
                                 color=vars_to_cols['acc_abs'],
                                 markerfacecolor=vars_to_cols['acc_abs'])
legendAccepted = mpl.lines.Line2D([],[],marker='',linewidth=5,
                                 color=vars_to_cols['acc_early'],
                                 markerfacecolor=vars_to_cols['acc_early'])

first_legend = plt.legend(loc = 'best', prop = {'size': 20},
           handles = [legendSent, legendReturned, legendAccepted],
           labels = ['Absentee issued', 'Absentee accepted', 'Early in-person'],
          )

proviEx = mpl.lines.Line2D([],[],marker='',linewidth=5,
                                 color='black',
                                 linestyle = 'dotted',
                                 markerfacecolor='black')
votedEx = mpl.lines.Line2D([],[],marker='',
                                 linewidth=5,
                                 color='black',
                                 linestyle = 'solid',
                                 markerfacecolor='black')
second_legend = plt.legend(loc = (0.02,0.65), prop = {'size': 12},
                           handles = [proviEx, votedEx],
                           handlelength = 3,
                           labels = ['2020', '2024'],
                                 )
plt.gca().add_artist(first_legend)
plt.gca().add_artist(second_legend)


print('plotting')
plt.savefig(FIG_NAME, dpi=400)
plt.close()
