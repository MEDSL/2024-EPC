#!/bin/bash

cd /d/research/eln24/scrapers

xvfb-run -a /usr/bin/python3 -W "ignore" FL_vbm_scraper.py >> errors.txt 2>&1
xvfb-run -a /usr/bin/python3 -W "ignore" PA_early_scraper.py >> errors.txt 2>&1

/usr/bin/python3 -W "ignore" /d/research/epc_dailies/infrastructure/early/FL/plot_FL_early.py >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
/usr/bin/python3 -W "ignore" /d/research/epc_dailies/infrastructure/early/TX/plot_TX_early.py >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
Rscript /d/research/epc_dailies/infrastructure/early/PA/PA_abs_2.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1

