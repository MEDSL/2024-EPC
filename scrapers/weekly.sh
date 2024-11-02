#!/bin/bash

cd /d/research/eln24/scrapers

/usr/bin/python3 -W "ignore" NC_registration_scraper.py >> errors.txt 2>&1
