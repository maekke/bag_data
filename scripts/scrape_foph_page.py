#!/bin/env python

import datetime
import re
from bs4 import BeautifulSoup
import requests

import common as c


def download_text(url, encoding='utf-8'):
    req = requests.get(url)
    req.raise_for_status()
    if encoding:
        req.encoding = encoding
    return req.text


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%d.%m.%Y, %H.%M')


def strip_number(number):
    return number.replace(' ', '')


def get_tests(soup):
    title = soup.find('h3', string=re.compile(r'Tests and share of positive tests'))
    par = title.find_next('p')
    date = c.search(r'Status: (\d+\.\d+\.20\d{2}, \d{2}\.\d{2})h', par.string)
    date = parse_date(date)

    total_tests = ''
    positivity_rate = ''
    total_antigen_tests = ''
    antigen_positivity_rate = ''

    table = title.find_next('table')
    for row in table.find_all('tr'):
        if c.search(r'^(PCR tests)', row.find_all('th')[0].text):
            total_tests = strip_number(row.find_all('td')[0].text)
        if c.search(r'^(Antigen tests)', row.find_all('th')[0].text):
            total_antigen_tests = strip_number(row.find_all('td')[0].text)
        if c.search(r'^(Share of positive PCR tests)', row.find_all('th')[0].text):
            positivity_rate = c.search(r'(\d+.*)%', row.find_all('td')[0].text)
            positivity_rate = positivity_rate.replace(',', '.')
        if c.search(r'^(Share of positive antigen tests)', row.find_all('th')[0].text):
            antigen_positivity_rate = c.search(r'(\d+.*)%', row.find_all('td')[0].text)
            antigen_positivity_rate = antigen_positivity_rate.replace(',', '.')

    return date, total_tests, positivity_rate, total_antigen_tests, antigen_positivity_rate


def get_isolated_quarantined(soup):
    title = soup.find('h3', string=re.compile(r'Contact tracing'))
    par = title.find_next('p')
    date = c.search(r'Status: (\d+\.\d+\.20\d{2}, \d{2}\.\d{2})h', par.string)
    date = parse_date(date)

    isolated = ''
    quarantined = ''
    travel_quarantined = ''

    table = title.find_next('table')
    for row in table.find_all('tr'):
        if c.search(r'^(In isolation)', row.find_all('th')[0].text):
            isolated = strip_number(row.find_all('td')[0].text)
        if c.search(r'^(In quarantine)', row.find_all('th')[0].text):
            quarantined = strip_number(row.find_all('td')[0].text)
        if c.search(r'^(Additionally in quarantine)', row.find_all('th')[0].text):
            travel_quarantined = strip_number(row.find_all('td')[0].text)

    return date, isolated, quarantined, travel_quarantined


URL = 'https://www.covid19.admin.ch/en/overview?ovTime=total'
content = download_text(URL)
soup = BeautifulSoup(content, 'html.parser')

date, total_tests, positivity_rate, total_antigen_tests, antigen_positivity_rate = get_tests(soup)
date_iso, isolated, quarantined, travel_quarantined = get_isolated_quarantined(soup)
assert date.date() == date_iso.date(), f'date mismatch: {date} != {date_iso}'

print(f'{date},{total_tests},{positivity_rate},{isolated},{quarantined},{travel_quarantined},{total_antigen_tests},{antigen_positivity_rate },{URL}')
