#!/bin/env python

import re
import sys

import common as c


def parse_pcr_tot_tests(txt):
    tot_tests = c.txt_to_int(c.search(r'insgesamt auf( .ber| rund| mehr als)? ([\d\s.]+)\.', txt, index=2))
    pcr_pos = txt.find('PCR-Tests')
    if tot_tests is None and pcr_pos > 0:
        # extract the line with Total / Totale Anzahl
        pcr_pos = txt.find('\n', pcr_pos) + 1
        pcr_end_pos = txt.find('\n', pcr_pos)
        line = txt[pcr_pos:pcr_end_pos]
        # replace whitespace between numbers '937 488' -> '937488'
        line = re.sub(r'(\d)\s(\d)', r'\1\2', line)
        # match the value
        pcr = re.compile(r'(Totale Anzahl|Total)\s+\+?(\d+)\s')
        res = pcr.match(line)
        if res is not None:
            tot_tests = c.txt_to_int(res[2])
            return tot_tests
        res = re.search(r'Total durchgef.hrte Tests\s+(\d+)\s+\+?\d+\s', line)
        if res is not None:
            tot_tests = c.txt_to_int(res[1])
    return tot_tests


def parse_data(filename):
    txt = c.pdf_to_text(filename)
    date_time = c.search(r'Stand (\d.*) Uhr', txt)
    if date_time is None:
        date = c.search(r'Stand\: (\d{2}\.\d{2}\.20\d{2})', txt)
        time = c.search(r'Zeit: (\d+:\d{2})', txt)
        if date is not None and time is not None:
            date_time = '{} {}'.format(date, time)
    date = c.parse_date(date_time)

    tot_tests = parse_pcr_tot_tests(txt)

    positivity_rate = c.txt_to_float(c.search(r'Bei (\d+)% dieser Tests fiel das Resultat positiv aus', txt))
    if positivity_rate is None:
        positivity_rate = c.txt_to_float(c.search(r'Positivit.tsrate( \*+| \(%\)|\*+)?\s+(\d\.?\d?)[%\s]', txt, index=2))
    if positivity_rate is None:
        positivity_rate = c.txt_to_float(c.search(r'Anteil positive Tests \(%\)(\d)?\s+(\d\.?\d?)[%\s]', txt, index=2))

    isolated = c.txt_to_int(c.search(r'(\d+)\s+(F.lle|Personen aufgrund einer laborbest.tigten COVID-19 Erkrankung)? in\sIsolation', txt, index=1))
    quarantined = c.txt_to_int(c.search(r'(\d+)\s?(in|Kontaktpersonen\sin\s.rztlich\sverordneter)? Quarant.ne', txt))
    quarantined_travel = None
    if isolated is None or quarantined is None:
        pos = txt.find('Contact Tracing')
        if pos > 0:
            pcr = re.compile(r'Total\s?(\*+|\(%\))?\s+(\d+)\s+(\d+\s?\d+|\d+)\s+(\d+\s?\d+|\d+)?')
            #pcr = re.compile(r'Total\s?(\*+|\(%\))?\s+(\d+)\s+(\d+)\s+(\d+|\d+\s?\d+)?')
            res = pcr.search(txt, pos)
            if res is not None:
                isolated = c.txt_to_int(res[2])
                quarantined = c.txt_to_int(res[3])
                quarantined_travel = c.txt_to_int(res[4].strip())

    print('{},{},{},{},{},{},{}'.format(date, tot_tests or '', positivity_rate or '', isolated or '', quarantined or '', quarantined_travel or '', filename))


if len(sys.argv) != 2:
    raise ValueError('please provide a file name as input!')

parse_data(sys.argv[1])
