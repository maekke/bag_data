#!/bin/env python

import datetime
import re
import subprocess

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

