"""Extract clean CSVs for Vega-Lite from the QILT SES 2025 tables and the
Dept of Education international student data (aggregated CSV).
Usage: python3 extract_ses.py NATIONAL.xlsx INTERNATIONAL.xlsx he_intl_by_nat_state.csv OUTDIR
"""
import sys, re, csv, collections, openpyxl

NAT, INT, PIV, OUT = sys.argv[1:5]
wbN = openpyxl.load_workbook(NAT, read_only=True, data_only=True)
wbI = openpyxl.load_workbook(INT, read_only=True, data_only=True)

def num(v):
    """'84.5 (83.9, 85.1)' -> 84.5 ; 'n/a' -> None ; '11,893' -> 11893"""
    if v is None: return None
    m = re.match(r'\s*([\d,]+\.?\d*)', str(v))
    return float(m.group(1).replace(',', '')) if m else None

def clean(s):
    return re.sub(r'[\s*†]+$', '', re.sub(r'^(Focus areas|Questionnaire item):\s*', '', str(s))).strip().replace('\xa0', ' ')

def table(wb, sheet, label_cols=1):
    """Return header list and rows [(labels..., values...)] from a QILT sheet."""
    rows = list(wb[sheet].iter_rows(values_only=True))
    hdr = None; out = []
    for i, r in enumerate(rows[3:], 3):
        cells = list(r)
        if hdr is None:
            hdr = [clean(c) for c in cells if c not in (None, '')]
            continue
        if all(c in (None, '') for c in cells): break
        nonblank = [c for c in cells if c not in (None,)]
        # strip leading empty strings
        while nonblank and nonblank[0] == '': nonblank.pop(0)
        if not nonblank: break
        out.append(nonblank)
    return hdr, out

def write(name, header, rows):
    with open(f'{OUT}/{name}', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print(f'{name}: {len(rows)} rows')

FOCUS = ['Skills Development', 'Peer Engagement', 'Teaching Quality and Engagement',
         'Student Support and Services', 'Learning Resources', 'Overall Educational Experience']
SHORT = ['skills', 'peer', 'teaching', 'support', 'resources', 'overall']

# ---- University locations (main campus, approximate; verify before publishing) ----
UNI_GEO = {
 'Australian Catholic University': ('NSW', -33.8389, 151.2070),
 'Australian University of Theology': ('NSW', -33.8700, 151.2070),
 'Avondale University': ('NSW', -33.0750, 151.4520),
 'Bond University': ('QLD', -28.0723, 153.4177),
 'Central Queensland University': ('QLD', -23.3229, 150.5195),
 'Charles Darwin University': ('NT', -12.3717, 130.8686),
 'Charles Sturt University': ('NSW', -35.0587, 147.3533),
 'Curtin University': ('WA', -32.0062, 115.8944),
 'Deakin University': ('VIC', -37.8470, 145.1150),
 'Edith Cowan University': ('WA', -31.7518, 115.7700),
 'Federation University Australia': ('VIC', -37.6276, 143.8904),
 'Flinders University': ('SA', -35.0213, 138.5720),
 'Griffith University': ('QLD', -27.5530, 153.0530),
 'James Cook University': ('QLD', -19.3283, 146.7585),
 'La Trobe University': ('VIC', -37.7210, 145.0480),
 'Macquarie University': ('NSW', -33.7738, 151.1126),
 'Monash University': ('VIC', -37.9105, 145.1362),
 'Murdoch University': ('WA', -32.0670, 115.8350),
 'Queensland University of Technology': ('QLD', -27.4772, 153.0280),
 'RMIT University': ('VIC', -37.8083, 144.9631),
 'Southern Cross University': ('NSW', -28.8197, 153.3010),
 'Swinburne University of Technology': ('VIC', -37.8221, 145.0389),
 'The Australian National University': ('ACT', -35.2777, 149.1185),
 'The University of Adelaide': ('SA', -34.9206, 138.6044),
 'The University of Melbourne': ('VIC', -37.7963, 144.9614),
 'The University of Notre Dame Australia': ('WA', -32.0560, 115.7470),
 'The University of Queensland': ('QLD', -27.4975, 153.0137),
 'The University of South Australia': ('SA', -34.9220, 138.5900),
 'The University of Sydney': ('NSW', -33.8888, 151.1873),
 'The University of Western Australia': ('WA', -31.9806, 115.8178),
 'Torrens University': ('SA', -34.9250, 138.6050),
 'University of Canberra': ('ACT', -35.2384, 149.0839),
 'University of Divinity': ('VIC', -37.8000, 145.0300),
 'University of New England': ('NSW', -30.4878, 151.6435),
 'University of New South Wales': ('NSW', -33.9173, 151.2313),
 'University of Newcastle': ('NSW', -32.8927, 151.7043),
 'University of Southern Queensland': ('QLD', -27.6050, 151.9320),
 'University of Tasmania': ('TAS', -42.9030, 147.3256),
 'University of Technology Sydney': ('NSW', -33.8832, 151.2005),
 'University of Wollongong': ('NSW', -34.4054, 150.8784),
 'University of the Sunshine Coast': ('QLD', -26.7180, 153.0640),
 'Victoria University': ('VIC', -37.7940, 144.8990),
 'Western Sydney University': ('NSW', -33.8136, 151.0215),
}
def uname(s): return re.sub(r'\*+$', '', str(s)).strip()

# 1. University x 6 focus areas (UG, 2025) + size + domestic/intl overall + location
_, uni = table(wbN, 'FOCUS_UG_UNI_1Y_INST_CI')
_, size = table(wbN, 'CHARINT_UG_UNI_1Y_INST')
sz = {uname(r[0]): (num(r[1]) or 0) + (num(r[3]) or 0) for r in size}
intl_share = {uname(r[0]): num(r[4]) for r in size}
_, e942 = table(wbN, 'FOCUS_UG_UNI_2Y_INST_CI_E942')
# column layout: per focus area 6 cols: 24D,24I,24T,25D,25I,25T -> 2025 overall = idx of last block
dom_int = {uname(r[0]): (num(r[1+30+3]), num(r[1+30+4])) for r in e942 if len(r) > 36}
_, intsat = table(wbI, 'INTSAT_UG_UNI_1Y_INST_CI')
living = {uname(r[0]): num(r[8]) for r in intsat}
rows = []
for r in uni:
    n = uname(r[0])
    if n == 'All Universities' or n not in UNI_GEO: continue
    st, lat, lon = UNI_GEO[n]
    d, i = dom_int.get(n, (None, None))
    rows.append([n, st, lat, lon, int(sz.get(n, 0)), intl_share.get(n)] +
                [num(v) for v in r[1:7]] + [d, i, living.get(n)])
write('uni_ug_2025.csv', ['university', 'state', 'lat', 'lon', 'ug_population', 'intl_pct'] + SHORT +
      ['overall_domestic', 'overall_international', 'intl_living_overall'], rows)

# 1b. State summary: population-weighted mean of universities in each state
agg = collections.defaultdict(lambda: [0.0] * 7)
for r in rows:
    w = r[4]
    a = agg[r[1]]; a[0] += w
    for k in range(6): a[k + 1] += w * (r[6 + k] or 0)
write('state_ug_2025.csv', ['state', 'ug_population'] + SHORT,
      [[s, int(a[0])] + [round(a[k] / a[0], 1) for k in range(1, 7)] for s, a in sorted(agg.items())])

# 2. Study area x 6 focus (UG universities, 2025) + sense of belonging
_, area = table(wbN, 'FOCUS_UG_UNI_1Y_AREA')
_, bel = table(wbN, 'BELONG_UG_ALL_17-YY_AREA')
belong = {clean(r[0]): num(r[-1]) for r in bel}
write('area_ug_2025.csv', ['study_area'] + SHORT + ['belonging'],
      [[clean(r[0])] + [num(v) for v in r[1:7]] + [belong.get(clean(r[0]))] for r in area if clean(r[0]) != 'Total'])

# 3. National trend 2017-2025 (UG, all providers), long format
_, tr = table(wbN, 'FOCUS_UG_ALL_17-YY_YEAR')
write('trend_ug.csv', ['year', 'focus_area', 'pct_positive'],
      [[int(str(r[0])[:4]), FOCUS[k], num(r[k + 1])] for r in tr for k in range(6)])

# 4. Demographic / contextual groups (UG universities, 2025)
_, sg = table(wbN, 'FOCUS_UG_UNI_1Y_SG')
write('groups_ug_2025.csv', ['group_type', 'group'] + SHORT,
      [[clean(r[0]), clean(r[1])] + [num(v) for v in r[2:8]] for r in sg if len(r) >= 8])

# 5. Individual question items, UG all providers, 2025 total (last column)
items = []
for pre, fa in [('DEVEL', 'Skills Development'), ('ENGAG', 'Peer Engagement'), ('TEACH', 'Teaching Quality and Engagement'),
                ('SUPP', 'Student Support and Services'), ('RESR', 'Learning Resources')]:
    _, t = table(wbN, f'{pre}_UG_ALL_17-YY_STAGE')
    for r in t:
        label = clean(r[0])
        if label == 'Overall Educational Experience': continue
        items.append([fa, re.sub(r'^[^:]+:\s*', '', label), num(r[-1])])
write('items_ug_2025.csv', ['focus_area', 'item', 'pct_positive'], items)

# 6. Reasons for considering leaving (UG all providers), 2023-2025 consistent wording
_, cs = table(wbN, 'CONSID_UG_ALL_17-YY_CH')
write('leave_reasons_ug.csv', ['reason', 'y2023', 'y2024', 'y2025'],
      [[clean(r[0])] + [num(v) for v in r[7:10]] for r in cs if num(r[9]) is not None])

# 7. International: domestic vs international by focus area (UG, 2025)
_, de = table(wbN, 'FOCUS_UG_ALL_17-YY_E942')
hdr = table(wbN, 'FOCUS_UG_ALL_17-YY_E942')[0]
dvi = []
for r in de:
    grp = clean(r[0])
    if grp not in ('Domestic', 'International'): continue
    for j, h in enumerate(hdr):
        if h.startswith('2025'):
            dvi.append([grp, clean(h.split(':', 1)[1]), num(r[j + 1])])
write('domestic_vs_intl_ug_2025.csv', ['student_type', 'focus_area', 'pct_positive'], dvi)

# 8. International: reasons for choosing Australia by home country (UG)
h, ra = table(wbI, 'INTAUS_UG_ALL_1Y_COUNTRY_CI')
write('intl_reasons_by_country_ug.csv', ['country', 'reason', 'pct_important'],
      [[clean(r[0]), h[k], num(r[k + 1])] for r in ra for k in range(len(h)) if num(r[k + 1]) is not None])

# 9. International: living experience by home country (UG)
h, lv = table(wbI, 'INTSAT_UG_ALL_1Y_COUNTRY_CI')
write('intl_living_by_country_ug.csv', ['country', 'aspect', 'pct_positive'],
      [[clean(r[0]), h[k], num(r[k + 1])] for r in lv for k in range(len(h)) if num(r[k + 1]) is not None])

# 10. Dept of Education: international HE enrolments by nationality x state
piv = list(csv.DictReader(open(PIV)))
my = [[r['state'], int(r['enrolments'])] for r in piv if r['year'] == '2025' and r['nationality'] == 'Malaysia' and r['state'] != 'NAT']
write('malaysia_he_by_state_2025.csv', ['state', 'enrolments'], my)
tr = collections.Counter()
for r in piv:
    if r['nationality'] == 'Malaysia': tr[int(r['year'])] += int(r['enrolments'])
write('malaysia_he_trend.csv', ['year', 'enrolments'], sorted(tr.items()))
tot = collections.Counter(); bystate = collections.Counter()
for r in piv:
    if r['year'] == '2025':
        tot[r['nationality']] += int(r['enrolments']); bystate[(r['nationality'], r['state'])] += int(r['enrolments'])
top = [n for n, _ in tot.most_common(10)]
write('top10_nationalities_by_state_2025.csv', ['nationality', 'state', 'enrolments'],
      [[n, s, c] for (n, s), c in sorted(bystate.items()) if n in top and s != 'NAT'])
