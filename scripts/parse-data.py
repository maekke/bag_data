#!/bin/env python

import re
import sys

from common import *

if len(sys.argv) != 2:
    raise ValueError('please provide a file name as input!')

filename = sys.argv[1]
txt = pdf_to_text(filename)
date_time = search(r'Stand (\d.*) Uhr', txt)
if date_time is None:
    date = search(r'Stand\: (\d{2}\.\d{2}\.20\d{2})', txt)
    time = search(r'Zeit: (\d+:\d{2})', txt)
    if date is not None and time is not None:
        date_time = '{} {}'.format(date, time)
date = parse_date(date_time)

tot_tests = txt_to_int(search(r'insgesamt auf( über| rund| mehr als)? ([\d\s’]+)\.', txt, index=2))
pcr_pos = txt.find('PCR-Tests')
if tot_tests is None and pcr_pos > 0:
    p = re.compile(r'Total\s+([\d\s]+)  ')
    m = p.search(txt, pcr_pos)
    if m is not None:
        tot_tests = txt_to_int(m[1])
if tot_tests is None and pcr_pos > 0:
    p = re.compile(r'Totale Anzahl\s+([\d\s]+)  ')
    m = p.search(txt, pcr_pos)
    if m is not None:
        tot_tests = txt_to_int(m[1])

positivity_rate = txt_to_float(search(r'Bei (\d+)% dieser Tests fiel das Resultat positiv aus', txt))
if positivity_rate is None:
    positivity_rate = txt_to_float(search('Positivit.tsrate( \*+| \(%\)|\*+)?\s+(\d\.?\d?)[%\s]', txt, index=2))

isolated = txt_to_int(search(r'(\d+)\s+(Fälle|Personen aufgrund einer laborbestätigten COVID-19 Erkrankung)? in\sIsolation', txt, index=1))
quarantined = txt_to_int(search(r'(\d+)\s?(in|Kontaktpersonen\sin\särztlich\sverordneter)? Quarantäne', txt))
quarantined_travel = None
if isolated is None and quarantined is None:
    pos = txt.find('Contact Tracing')
    if pos > 0:
        p = re.compile(r'Total\s?(\*+|\(%\))?\s+(\d+)\s+(\d+)\s+(\d+\s?\d+|\d+)?')
        m = p.search(txt, pos)
        if m is not None:
            isolated = txt_to_int(m[2])
            quarantined = txt_to_int(m[3])
            quarantined_travel = txt_to_int(m[4])

print('{},{},{},{},{},{},{}'.format(date, tot_tests or '', positivity_rate or '', isolated or '', quarantined or '', quarantined_travel or '', filename))
