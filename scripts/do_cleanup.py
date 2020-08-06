#!/usr/bin/env python

import csv
import sys


def update_value_if_needed(data, date, row, column_name, check_mismatch=True):
    if data[date][column_name] == "":
        data[date][column_name] = row[column_name]
    elif check_mismatch and data[date][column_name] != row[column_name] and row[column_name] != "":
        print('Warning data mismatch @ {}, column {} contains "{}" and should be replaced with "{}"'.format(date, column_name, data[date][column_name], row[column_name]))


def read_file(file_name):
    data = {}
    with open(file_name, encoding='utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            # date,total_number_of_tests,positivity_rate_percent,isolated,quarantined,quarantined_travel,source_file
            date = row["date"]
            if date not in data:
                data[date] = row
            else:
                for column in ["total_number_of_tests", "positivity_rate_percent", "isolated", "quarantined", "quarantined_travel"]:
                    update_value_if_needed(data, date, row, column)
                update_value_if_needed(data, date, row, "source_file", check_mismatch=False)
    return data


def write_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as csvfile:
        spamwriter = csv.DictWriter(csvfile, ["date", "total_number_of_tests", "positivity_rate_percent", "isolated", "quarantined", "quarantined_travel", "source_file"], delimiter=',', quotechar='"', lineterminator='\n')
        spamwriter.writeheader()
        for key, value in data.items():
            spamwriter.writerow(value)


if len(sys.argv) != 2:
    raise ValueError('provide a filename as input!')

file_contents = read_file(sys.argv[1])
write_file(sys.argv[1], file_contents)
