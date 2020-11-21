#!/usr/bin/env python

import csv
import sys


def read_file(file_name):
    data = {}
    with open(file_name, encoding='utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            # date,total_number_of_tests,positivity_rate_percent,isolated,quarantined,quarantined_travel,source_file
            date = row["date"]
            data[date] = row
    return data


def write_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as csvfile:
        spamwriter = csv.DictWriter(csvfile, ["date", "total_number_of_tests", "positivity_rate_percent", "isolated", "quarantined", "quarantined_travel", "total_number_of_antigen_tests", "positivity_rate_antigen_tests", "source_file"], delimiter=',', quotechar='"', lineterminator='\n')
        spamwriter.writeheader()
        for _, value in data.items():
            spamwriter.writerow(value)


if len(sys.argv) != 2:
    raise ValueError('provide a filename as input!')

file_contents = read_file(sys.argv[1])
write_file(sys.argv[1], file_contents)
