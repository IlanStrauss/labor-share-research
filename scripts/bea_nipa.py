"""
BEA NIPA annual data, in millions of current dollars, as {series_code: {year: value}}.

load() reads data/bea_nipa_extract.csv, the saved extract of every series this note uses,
so all published numbers reproduce exactly. scripts/fetch_data.py rebuilds that extract
from BEA's bulk file (public, no API key needed):
https://apps.bea.gov/national/Release/TXT/NipaDataA.txt (~12 MB, all NIPA tables),
saved to data/bea_raw/, which git ignores. Series codes are listed in BEA's
SeriesRegister.txt, next to the data file.
"""

import csv
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(ROOT, 'data', 'bea_nipa_extract.csv')
RAW_FILE = os.path.join(ROOT, 'data', 'bea_raw', 'NipaDataA.txt')
URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'


def load(path=EXTRACT):
    data = {}
    with open(path, newline='') as f:
        for r in csv.DictReader(f):
            data.setdefault(r['series_code'], {})[int(r['year'])] = float(r['value_millions'])
    return data


def load_bulk(path=RAW_FILE):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"Downloading BEA NIPA bulk file to {path} ...")
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(path, 'wb') as f:
            f.write(resp.read())
    data = {}
    with open(path, encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        next(rows)
        for code, period, value in rows:
            if not period.isdigit():
                continue
            try:
                data.setdefault(code, {})[int(period)] = float(value.replace(',', ''))
            except ValueError:
                continue
    return data
