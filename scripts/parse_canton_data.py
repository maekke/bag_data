#!/bin/env python

import sys
import re

import common as c


def parse_canton_data(canton, filename):
    txt = c.pdf_to_text(filename)

    # pylint: disable=W0105
    """
    Coronavirus-Krankheit-2019 (COVID-19)
    Eidgen<C3><B6>ssisches Departement des Innern EDI
    Bundesamt f<C3><BC>r Gesundheit BAG
    Direktionsbereich <C3><96>ffentliche Gesundheit
    Situationsbericht zur epidemiologischen Lage in der Schweiz
    und im F<C3><BC>rstentum Liechtenstein - Woche 28 (06.-12.07.2020)
    """

    week = c.search(r'Liechtenstein - Woche (\d+)', txt)

    """
    Canton, tests of previous-week then current-week

    AG 5478 3588 808 529 1.3 1.8
    AI 96 55 595 341 0.0 0.0
    AR 391 249 708 451 0.5 1.2
    BE 6924 4652 669 449 0.4 0.9
    ...
    """
    start = txt.find('Anzahl PCR-Tests in der Schweiz')
    if start == -1:
        start = txt.find('Anzahl durchgeführte PCR-Tests in der Schweiz')
    if start > 0:
        start = txt.find(r' AG ', start)
    else:
        start = 0
    end = txt.find('Tabelle 4. Durchgeführte Tests nach Kalenderwoche', start)
    if end == -1:
        end = txt.find('Die Altersverteilung der', start)
    if end > start > 0 and end > start:
        tests_table = txt[start:end]
        # the numbers are sometimes separated with spaces for >1k values
        pcr = re.compile('(\d+)\s(\d+)')
        tests_table = pcr.sub(r'\1\2', tests_table)
        number_of_tests = c.txt_to_int(c.search(r'(\n\s+)?{}\s+\d+\s+(\d+)'.format(canton), tests_table, index=2))
        positivity_rate = c.txt_to_float(c.search(r'(\n\s+)?{}\s+.*([0-9]+\.[0-9]+)\n'.format(canton), tests_table, index=2))

    print('{},{},{},{}'.format(week, number_of_tests or '', positivity_rate or 0.0, filename))


if len(sys.argv) != 3:
    raise ValueError('please provide a canton and file name as input!')

parse_canton_data(sys.argv[1], sys.argv[2])
