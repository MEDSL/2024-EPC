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
CURR_DATE_MAX = datetime(year=datetime.today().year,
                         month=datetime.today().month,
                         day=datetime.today().day-1, #x-axis ends yesterday
                         hour=20)

def BuildDf(fnames):
    ad = pd.DataFrame(index = range(len(fnames)),
                      columns = ['day','act','inact','prov']
                     )
    for i in range(len(fnames)):
        fname = fnames[i]
        if r".csv" in fname:
            #It seems that two different encodings are used for the csv files
            try:
                curr = pd.read_csv(fname, sep="\t", encoding="utf-8")
            except:
                curr = pd.read_csv(fname, sep="\t", encoding="utf-16")
        elif r".xlsx" in fname:
            curr = pd.read_excel(fname)
        #ADJUST FOR YOUR DIRECTORY STRUCTURE
        dateLoc = fname.find('raw/') + len('raw/')
        dateStr = fname[dateLoc:dateLoc+8]
        ad.iloc[i].day = datetime.strptime(dateStr,'%Y%m%d').date()
        curr.columns = ['county','act','inact','prov','total']
        act = curr.loc[curr.county=='Grand Total', 'act']
        inact = curr.loc[curr.county=='Grand Total', 'inact']
        prov = curr.loc[curr.county=='Grand Total', 'prov']
        ad.iloc[i].act = int(act.astype(str).str.replace(',',''))
        ad.iloc[i].inact = int(inact.astype(str).str.replace(',',''))
        ad.iloc[i].prov = int(prov.astype(str).str.replace(',',''))
    return(ad)
     

################################################################################
# Generate data
################################################################################
fnames = os.listdir(f'{BASE_DIR}raw/')
fnames = [f'{BASE_DIR}raw/' + _ for _ in fnames]
fnames = [_ for _ in fnames if '~' not in _]

reg = BuildDf(fnames)

reg.day = pd.to_datetime(reg.day, format='%Y-%m-%d')
reg = reg.sort_values(by='day')


################################################################################
# Plot
################################################################################
plt.rcParams["figure.figsize"] = (10,8)
plt.gcf().subplots_adjust(bottom=0.15,left=0.175,right=0.95)
plt.title(f'Montana Registered Voters {DATE_TO_PRINT}',
          size = 25, pad = 15)
plt.figtext(0.025,0.03,
"Data from Montana Secretary of State, sosmt.gov/elections/regvotercounty/")
plt.figtext(0.025,0.0075,
"Graph from MIT Election Data and Science Lab, @MITelectionlab",
            size = 10)
plt.yticks(fontsize=15)
plt.xticks(fontsize=11)
format_date = mpl.dates.DateFormatter('%b %d')
plt.gca().xaxis.set_major_formatter(format_date)
plt.gca().xaxis.set_major_locator(mpl.dates.DayLocator(interval=7))
plt.xlim((datetime(year=2024,month=8,day=15,hour=12),
          CURR_DATE_MAX
          ))
plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylabel("Number of Registered Voters", size = 18, labelpad = 20)
plt.xlabel("Data as of", size = 18, labelpad = 20)

vars_to_cols = {
                'act': medslDarkGreen,
                'inact': medslGold,
                'prov': medslLightPurple,
                }
plt.grid(alpha=0.75)

for var in vars_to_cols.keys():
    plt.plot_date(list(reg['day']), list(reg[var]),
                  linewidth=5, color = vars_to_cols[var],
                  ms = 12,
                  linestyle = 'solid')

legendAct = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                              color=vars_to_cols['act'],
                              markerfacecolor=vars_to_cols['act'])
legendIna = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color=vars_to_cols['inact'],
                                 markerfacecolor=vars_to_cols['inact'])
legendPro = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color=vars_to_cols['prov'],
                                 markerfacecolor=vars_to_cols['prov'])
legend = plt.legend(loc = 'center left', prop = {'size': 20},
    handles = [legendAct, legendIna, legendPro],
    labels = ['Active', 'Inactive', 'Provisional'],
          )
plt.gca().add_artist(legend)
plt.savefig(FIG_NAME, dpi=400)
plt.close()

plotDataName = date.today().strftime("%Y%m%d")
reg.to_csv(BASE_DIR+'plot_data/'+plotDataName+'_MT_reg.csv',
           encoding='utf-8', index=False)
