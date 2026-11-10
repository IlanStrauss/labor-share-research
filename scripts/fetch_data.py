"""
Download every dataset the note uses and save it under data/, so that the analysis scripts
run offline and reproduce the published numbers exactly. Run it only to move to newer data,
then rerun the analysis scripts and update the text. See data/README.md.

Run:  python3 scripts/fetch_data.py              (everything)
      python3 scripts/fetch_data.py pwt bls      (only the parts named: bea, pwt, bls)

Writes
- data/bea_nipa_extract.csv: the BEA NIPA annual series listed in SERIES below, from BEA's bulk
  file. An existing data/bea_raw/NipaDataA.txt is reused; delete it to download BEA's latest.
- data/pwt_labor_share.csv: Penn World Table 11.0 labor share (labsh), every country, from the
  publisher's archive on DataverseNL (doi:10.34894/FABVLR).
- data/bls_nonfarm_labor_share.csv: BLS labor share index for the nonfarm business sector (series PRS85006173),
  from the BLS public API.
"""

import csv
import io
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import EXTRACT, ROOT, load_bulk  # noqa: E402

DATA = os.path.join(ROOT, 'data')
REGISTER_URL = 'https://apps.bea.gov/national/Release/TXT/SeriesRegister.txt'

# Every BEA series the scripts read
SERIES = [
    'A261RC',  # Gross domestic income
    'A4002C',  # Compensation of employees, paid
    'A4102C',  # Wages and salaries (Table 1.10; W270RC is only its 'to persons' part)
    'B039RC',  # Employer contributions for government social insurance
    'B040RC',  # Employer contributions for employee pension and insurance funds
    'A262RC',  # Consumption of fixed capital (depreciation)
    'W271RC',  # Net operating surplus
    'W056RC',  # Taxes on production and imports
    'A107RC',  # Subsidies
    'A041RC',  # Proprietors' income with IVA and CCAdj
    'A048RC',  # Rental income of persons with CCAdj
    'W255RC',  # Net interest and miscellaneous payments on assets (national)
    'W272RC',  # Net interest and miscellaneous payments, domestic industries
    'A053RC',  # Corporate profits before tax without IVA and CCAdj
    'A054RC',  # Taxes on corporate income
    'A055RC',  # Corporate profits after tax without IVA and CCAdj
    'A059RC',  # Corporate capital consumption adjustment
    'A438RC',  # Consumption of fixed capital, corporate business
    'A264RC', 'A754RC', 'B188RC', 'Y080RC', 'Y083RC',  # depreciation by type of asset (Table 5.2.5)
    'A034RC',  # Wage and salary accruals
    'A064RC',  # Personal interest income
    'B703RC',  # Personal dividend income
    'B231RC', 'B245RC',  # Federal, and state and local, personal income taxes
    'A1587C', 'CON544', 'CON550', 'B738RC',  # Employee contributions for government social insurance
    'A445RC',  # Corporate profits with IVA and CCAdj, domestic industries
    'A191RC',  # Gross domestic product
    'A765RC', 'A194RC', 'A265RC',  # General government: value added, compensation, depreciation
    'A2009C',  # Gross housing value added
]

PWT_XLSX = 'https://dataverse.nl/api/access/datafile/554105'  # pwt110.xlsx, Penn World Table 11.0
BLS = 'PRS85006173'
BLS_API = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'


def get(url, tries=3, raw=False):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
                return body if raw else body.decode('utf-8-sig')
        except OSError:
            if i == tries - 1:
                raise
            time.sleep(30)


def write(name, header, rows):
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"Wrote data/{name} ({len(rows)} rows)")


def bea():
    d = load_bulk()
    names = {}
    for r in csv.reader(io.StringIO(get(REGISTER_URL))):
        if r and r[0] in SERIES:
            names[r[0]] = r[1]
    missing = [c for c in SERIES if c not in d]
    assert not missing, f'not in the BEA file: {missing}'
    write(os.path.basename(EXTRACT), ['series_code', 'series_name', 'year', 'value_millions'],
          [(c, names.get(c, ''), y, d[c][y]) for c in SERIES for y in sorted(d[c])])


def xlsx_rows(blob, sheet):
    # Rows of one worksheet as lists of strings, read with the standard library only
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    z = zipfile.ZipFile(io.BytesIO(blob))
    shared = [''.join(t.text or '' for t in si.iter(f"{{{ns['m']}}}t"))
              for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
    col = lambda ref: sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(re.match('[A-Z]+', ref).group())))
    for _, row in ET.iterparse(z.open(f'xl/worksheets/{sheet}.xml')):
        if row.tag != f"{{{ns['m']}}}row":
            continue
        cells = {}
        for c in row.findall('m:c', ns):
            v = c.find('m:v', ns)
            if v is not None:
                cells[col(c.get('r'))] = shared[int(v.text)] if c.get('t') == 's' else v.text
        row.clear()
        yield [cells.get(i, '') for i in range(1, max(cells, default=0) + 1)]


def pwt():
    rows = xlsx_rows(get(PWT_XLSX, raw=True), 'sheet3')  # sheet3 is the Data sheet
    head = next(rows)
    i = {k: head.index(k) for k in ('countrycode', 'country', 'year', 'labsh')}
    out = [(r[i['countrycode']], r[i['country']], int(float(r[i['year']])), round(100 * float(r[i['labsh']]), 4))
           for r in rows if len(r) > i['labsh'] and r[i['labsh']] not in ('', 'NA')]
    write('pwt_labor_share.csv', ['iso3c', 'country', 'year', 'labor_share_pct'], out)


def bls():
    # The keyless API returns at most 10 years per request
    rows = []
    for start in range(1947, time.localtime().tm_year + 1, 10):
        body = json.dumps({'seriesid': [BLS], 'startyear': str(start), 'endyear': str(start + 9)}).encode()
        req = urllib.request.Request(BLS_API, data=body, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.load(r)
        assert res['status'] == 'REQUEST_SUCCEEDED', res.get('message')
        rows += [(int(x['year']), x['period'], float(x['value'])) for x in res['Results']['series'][0]['data']]
        time.sleep(2)
    write('bls_nonfarm_labor_share.csv', ['year', 'period', 'index_2017_100'], sorted(rows))


PARTS = {'bea': bea, 'pwt': pwt, 'bls': bls}


def main(parts):
    for name in parts or PARTS:
        PARTS[name]()


if __name__ == '__main__':
    main(sys.argv[1:])
