#!/bin/env python

import re
import sys

import common as c


def parse_data(filename):
    txt = c.pdf_to_text(filename)
    date_time = c.search(r'Stand (\d.*) Uhr', txt)
    if date_time is None:
        date = c.search(r'Stand\: (\d{2}\.\d{2}\.20\d{2})', txt)
        time = c.search(r'Zeit: (\d+:\d{2})', txt)
        if date is not None and time is not None:
            date_time = '{} {}'.format(date, time)
    date = c.parse_date(date_time)

    tot_tests = c.txt_to_int(c.search(r'insgesamt auf( über| rund| mehr als)? ([\d\s’]+)\.', txt, index=2))
    pcr_pos = txt.find('PCR-Tests')
    if tot_tests is None and pcr_pos > 0:
        pcr = re.compile(r'Total\s+([\d\s]+)  ')
        res = pcr.search(txt, pcr_pos)
        if res is not None:
            tot_tests = c.txt_to_int(res[1])
    if tot_tests is None and pcr_pos > 0:
        pcr = re.compile(r'Totale Anzahl\s+([\d\s]+)  ')
        res = pcr.search(txt, pcr_pos)
        if res is not None:
            tot_tests = c.txt_to_int(res[1])

    positivity_rate = c.txt_to_float(c.search(r'Bei (\d+)% dieser Tests fiel das Resultat positiv aus', txt))
    if positivity_rate is None:
        positivity_rate = c.txt_to_float(c.search('Positivit.tsrate( \*+| \(%\)|\*+)?\s+(\d\.?\d?)[%\s]', txt, index=2))

    isolated = c.txt_to_int(c.search(r'(\d+)\s+(Fälle|Personen aufgrund einer laborbestätigten COVID-19 Erkrankung)? in\sIsolation', txt, index=1))
    quarantined = c.txt_to_int(c.search(r'(\d+)\s?(in|Kontaktpersonen\sin\särztlich\sverordneter)? Quarantäne', txt))
    quarantined_travel = None
    if isolated is None and quarantined is None:
        pos = txt.find('Contact Tracing')
        if pos > 0:
            pcr = re.compile(r'Total\s?(\*+|\(%\))?\s+(\d+)\s+(\d+)\s+(\d+\s?\d+|\d+)?')
            res = pcr.search(txt, pos)
            if res is not None:
                isolated = c.txt_to_int(res[2])
                quarantined = c.txt_to_int(res[3])
                quarantined_travel = c.txt_to_int(res[4])

    print('{},{},{},{},{},{},{}'.format(date, tot_tests or '', positivity_rate or '', isolated or '', quarantined or '', quarantined_travel or '', filename))


if len(sys.argv) != 2:
    raise ValueError('please provide a file name as input!')

parse_data(sys.argv[1])
