#!/bin/bash

cd /d/research/eln24/scrapers

/usr/bin/python3 -W "ignore" PA_registration_scraper.py >> errors.txt 2>&1
/usr/bin/python3 -W "ignore" PA_mail_scraper.py >> errors.txt 2>&1
/usr/bin/python3 -W "ignore" MI_registration_scraper.py >> errors.txt 2>&1
/usr/bin/python3 -W "ignore" NC_registration_scraper.py >> errors.txt 2>&1
xvfb-run -a /usr/bin/python3 -W "ignore" SC_registration_scraper.py >> errors.txt 2>&1
xvfb-run -a /usr/bin/python3 -W "ignore" NC_early_scraper.py >> errors.txt 2>&1
xvfb-run -a /usr/bin/python3 -W "ignore" WI_early_scraper.py >> errors.txt 2>&1
xvfb-run -a /usr/bin/python3 -W "ignore" FL_registration_scraper.py >> errors.txt 2>&1
xvfb-run -a /usr/bin/python3 -W "ignore" TX_early_scraper.py >> errors.txt 2>&1

Rscript /d/research/epc_dailies/infrastructure/reg/MI/MI_reg.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
Rscript /d/research/epc_dailies/infrastructure/reg/PA/PA_reg.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
Rscript /d/research/epc_dailies/infrastructure/reg/FL/FL_reg.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
Rscript /d/research/epc_dailies/infrastructure/reg/WI/WI_reg.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
Rscript /d/research/epc_dailies/infrastructure/early/WI/WI_abs.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1
Rscript /d/research/epc_dailies/infrastructure/reg/NC/NC_reg.R >> /d/research/epc_dailies/infrastructure/errors.txt 2>&1

/usr/bin/python3 -W "ignore" SlackMessage.py >> errors.txt 2>&1
