#!/bin/bash

out_file="bag_data.csv"
python ./scripts/scrape_foph_page.py >> ./${out_file}
