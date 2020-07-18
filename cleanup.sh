#!/bin/bash

in_file="bag_data.csv"
out_file="bag_data_cleanup.csv"

head -n 1 ${in_file} > ${out_file}
# make each line unique based on the date+time column
tail -n +2 ${in_file} | sort -u -t, -k1,1 >> ${out_file}

mv ${out_file} ${in_file}
