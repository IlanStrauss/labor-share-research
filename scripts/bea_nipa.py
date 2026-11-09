"""
Load BEA's NIPA annual bulk file (public, no API key needed).

On first use, downloads https://apps.bea.gov/national/Release/TXT/NipaDataA.txt
(~12 MB, all NIPA tables) to data/bea_raw/, which git ignores. Returns
{series_code: {year: value}}, values in millions of current dollars.
Series codes are listed in BEA's SeriesRegister.txt, next to the data file.
"""

import csv
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_FILE = os.path.join(ROOT, 'data', 'bea_raw', 'NipaDataA.txt')
URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'


def load(path=RAW_FILE):
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
