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
                      columns = ['day','year','month','dem','rep','non','lib']
                     )
    for i in range(len(fnames)):
        fname = fnames[i]
        #ADJUST FOR YOUR DIRECTORY STRUCTURE
        start_loc = fname.find('raw/') + len('raw/')
        dateStr = fname[start_loc:start_loc+8]

        ad.iloc[i].day = datetime.strptime(dateStr,'%Y%m%d').date()
        ad.iloc[i].year = datetime.strptime(dateStr,'%Y%m%d').date().year       
        ad.iloc[i].month = datetime.strptime(dateStr,'%Y%m%d').date().month

        curr = pd.read_csv(fname, sep=",", encoding="utf-8")
        curr = curr.loc[curr.dist == 2]
        curr = pd.melt(curr, value_name='reg', var_name='party')
        curr = curr.loc[(curr.party != 'dist') & (curr.party != 'total')]
    
        dem = curr.loc[curr.party == 'Democratic', 'reg'].values[0]
        rep = curr.loc[curr.party == 'Republican', 'reg'].values[0]
        non = curr.loc[curr.party == 'Nonpartisan', 'reg'].values[0]
        lib = curr.loc[curr.party == 'Libertarian', 'reg'].values[0]

        ad.iloc[i].dem = int(dem)
        ad.iloc[i].rep = int(rep)
        ad.iloc[i].non = int(non)
        ad.iloc[i].lib = int(lib)
    return(ad)
     

################################################################################
# Generate data
################################################################################
fnames = os.listdir(f'{BASE_DIR}raw/')
fnames = [f'{BASE_DIR}raw/' + _ for _ in fnames]
fnames = [_ for _ in fnames if '~' not in _]

reg = BuildDf(fnames)

reg = reg.sort_values(by='day')
reg.reset_index(inplace=True, drop=True)


################################################################################
# Plot
################################################################################
plt.rcParams["figure.figsize"] = (10,8)
plt.gcf().subplots_adjust(bottom=0.15,left=0.175,right=0.95)
plt.title(f'Registered Voters in Nebraska CD2 {DATE_TO_PRINT}',
          size = 22, pad = 15)
plt.figtext(0.025,0.03,
"Data from Nebraska Secretary of State, "+\
"sos.nebraska.gov/elections/voter-registration-statistics")
plt.figtext(0.025,0.0075,
"Graph from MIT Election Data and Science Lab, @MITelectionlab",
            size = 10)
plt.yticks(fontsize=15)
xLabs = [_ + ' 1' for _ in \
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
         'Oct', 'Nov', 'Dec']]
xVals = [_+1 for _ in range(len(xLabs))]
plt.xticks(xVals, xLabs, fontsize=11)
plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylabel("Number of Registered Voters of Each Party", size = 18, labelpad = 20)
plt.xlabel("Data as of", size = 18, labelpad = 20)

vars_to_cols = {
                'dem': medslLogoBlue,
                'rep': medslLogoRed,
                'lib': medslYellow,
                'non': medslChartGrey
                }
plt.grid(alpha=0.75)

for year in [2020,2024]:
    plotDf = reg.loc[reg.year == year]
    if year == 2020:
        theLineStyle = 'dashed'
    else:
        theLineStyle = 'solid'
    for var in vars_to_cols.keys():
        plt.plot(list(plotDf['month']),
                 list(plotDf[var]),
                 linewidth=5,
                 marker='o',
                 color = vars_to_cols[var],
                 ms = 12,
                 linestyle = theLineStyle)

legendDem = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                              color=vars_to_cols['dem'],
                              markerfacecolor=vars_to_cols['dem'])
legendRep = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color=vars_to_cols['rep'],
                                 markerfacecolor=vars_to_cols['rep'])
legendNpa = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color=vars_to_cols['non'],
                                 markerfacecolor=vars_to_cols['non'])
legendLib = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color=vars_to_cols['lib'],
                                 markerfacecolor=vars_to_cols['lib'])
currEx = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color='black',
                                 markerfacecolor='black')
prevEx = mpl.lines.Line2D([],[],marker='o',linewidth=5,ms=10,
                                 color='black',
                                 linestyle = 'dotted',
                                 markerfacecolor='black')
first_legend = plt.legend(loc = (0.02, 0.2), prop = {'size': 20},
    handles = [legendDem, legendRep, legendNpa, legendLib],
    labels = ['Democrat', 'Republican', 'Nonpartisan', 'Libertarian'],
          )
second_legend = plt.legend(loc = (0.76, 0.275), prop = {'size': 20},
                           handles = [prevEx, currEx],
                           labels = ['2020', '2024'],
                                 )
plt.gca().add_artist(first_legend)
plt.gca().add_artist(second_legend)
plt.savefig(FIG_NAME, dpi=400)
plt.close()

plotDataName = date.today().strftime("%Y%m%d")
reg.to_csv(BASE_DIR+'plot_data/'+plotDataName+'_NE_reg.csv',
           encoding='utf-8', index=False)
