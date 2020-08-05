#!/bin/env python
""" common helper functions """

import datetime
import re
import subprocess


def pdf_to_text(path):
    """ reads given pdf file and returns it's textual contents """
    pdf_command = ['pdftotext', '-layout', path, '-']
    with subprocess.Popen(pdf_command, stdout=subprocess.PIPE) as text:
        out = text.stdout.read()
        text.wait()
        return out.decode('utf-8')


def search(pattern, text, index=1):
    """ find the pattern in text and return the contents when available """
    res = re.search(pattern, text)
    if res:
        return res[index]
    return None


def txt_to_int(txt):
    """ text to int convenience function """
    if txt is not None:
        txt = txt.replace(' ', '')
        txt = txt.replace('’', '')
        if len(txt) > 0:
            return int(txt)
    return None


def txt_to_float(txt):
    """ text to float convenience function """
    if txt is not None:
        txt = txt.replace(' ', '')
        if len(txt) > 0:
            return float(txt)
    return None


def parse_date(date_str):
    """ text to date parsing convenience function """
    date_str = date_str.replace('/', '.')
    date_str = date_str.replace(',', '')
    return datetime.datetime.strptime(date_str, '%d.%m.%Y %H:%M')
