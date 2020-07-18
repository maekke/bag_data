#!/bin/env python

import datetime
import re
import subprocess
import sys

def pdf_to_text(path):
    pdf_command = ['pdftotext', '-layout', path, '-']
    with subprocess.Popen(pdf_command, stdout=subprocess.PIPE) as text:
        t = text.stdout.read()
        text.wait()
        return t.decode('utf-8')

def search(pattern, text, index=1):
    res = re.search(pattern, text)
    if res:
        return res[index]
    return None

def txt_to_int(txt):
    if txt is not None:
        txt = txt.replace(' ', '')
        txt = txt.replace('’', '')
        if len(txt) > 0:
            return int(txt)
    return None

def parse_date(date_str):
    date_str = date_str.replace('/', '.')
    date_str = date_str.replace(',', '')
    return datetime.datetime.strptime(date_str, '%d.%m.%Y %H:%M')

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

isolated = txt_to_int(search(r'(\d+)\s+(Fälle|Personen aufgrund einer laborbestätigten COVID-19 Erkrankung)? in\sIsolation', txt, index=1))
quarantined = txt_to_int(search(r'(\d+)\s?(in|Kontaktpersonen\sin\särztlich\sverordneter)? Quarantäne', txt))
if isolated is None and quarantined is None:
    pos = txt.find('Contact Tracing')
    if pos > 0:
        p = re.compile(r'Total.*\s+(\d+)\s+(\d+)')
        m = p.search(txt, pos)
        if m is not None:
            isolated = txt_to_int(m[1])
            quarantined = txt_to_int(m[2])

print('{},{},{},{},{}'.format(date, tot_tests or '', isolated or '', quarantined or '', filename))
