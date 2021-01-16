#!/bin/env python

import re
import sys

import common as c


def parse_weekly_data(filename):
    txt = c.pdf_to_text(filename)
    txt = re.sub(r'(\d)\s(\d)', r'\1\2', txt)

    year = c.search(r'Stand:\s\d+\.\d+\.(\d{4})', txt)
    week = int(c.search(r'Liechtenstein - Woche (\d+) ', txt))

    tot_tests = ''
    tot_antigen_tests = ''
    pcr_pos = txt.find('Durchgeführte Tests')
    if pcr_pos > 0:
        pcr_pos = txt.find('PCR', pcr_pos)
        pcr_end_pos = txt.find('\n', pcr_pos)
        assert pcr_end_pos > pcr_pos
        line = txt[pcr_pos:pcr_end_pos]

        #line = re.sub(r'(\d)\s(\d)', r'\1\2', line)
        line = re.sub(r'\s+', r' ', line)
        tot_tests = c.txt_to_int(line.split(' ')[-2])

        # Antigen tests
        pcr_pos = txt.find('Antigen-Schnelltests', pcr_pos)
        pcr_end_pos = txt.find('\n', pcr_pos)
        assert pcr_end_pos > pcr_pos
        line = txt[pcr_pos:pcr_end_pos]
        line = re.sub(r'\s+', r' ', line)
        tot_antigen_tests = c.txt_to_int(line.split(' ')[-2])

    positivity_rate = ''
    antigen_positivity_rate = ''
    positivity_pos = txt.find('\nPositivit')
    if positivity_pos == -1:
        positivity_pos = txt.find('\nAnteil positiver Tests')
    if positivity_pos > 0:
        positivity_pos = txt.find('PCR', positivity_pos)
        positivity_end_pos = txt.find('\n', positivity_pos)
        assert positivity_end_pos > positivity_pos
        line = txt[positivity_pos:positivity_end_pos]
        line = re.sub(r'\s+', r' ', line)
        positivity_rate = line.split(' ')[-1]
        positivity_rate = c.txt_to_float(positivity_rate.replace('%', ''))

        # Antigen tests
        positivity_pos = txt.find('Antigen-Schnelltest', positivity_pos)
        positivity_end_pos = txt.find('\n', positivity_pos)
        assert positivity_end_pos > positivity_pos
        line = txt[positivity_pos:positivity_end_pos]
        line = re.sub(r'\s+', r' ', line)
        antigen_positivity_rate = line.split(' ')[-1]
        try:
            antigen_positivity_rate = c.txt_to_float(positivity_rate.replace('%', ''))
        except:
            pass

    print(f'{year},{week},{tot_tests},{positivity_rate},{tot_antigen_tests},{antigen_positivity_rate},{filename}')


if len(sys.argv) != 2:
    raise ValueError('please provide a file name as input!')

parse_weekly_data(sys.argv[1])
