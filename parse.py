import csv
import sys
import json
from dateutil.parser import parse
import time

if len(sys.argv) < 2:
  print 'specify file'
  exit(1)

f = sys.argv[1]

whales = {}

with open(f) as csvfile:
  reader = csv.DictReader(csvfile)
  badrows = 0
  emptyrows = 0
  rows = 0
  for row in reader:
    if row['Comment'] or row['Quality'] not in ['A', 'B', '1']:
      badrows += 1
      continue
    if not row['Ptt']:
      emptyrows += 1
      continue
    dt = parse(row['Date'], dayfirst=True)
    lat = float(row['Latitude'])
    lng = float(row['Longitude'])
    if row['Ptt'] not in whales:
      epoch = dt
      epochIso = dt.isoformat() + 'Z'
      whales[row['Ptt']] = {'epoch': epochIso, 'cartographicDegrees': [0, lng, lat, 0]}
    else:
      diff = dt - epoch
      diff = int(diff.total_seconds())
      whales[row['Ptt']]['cartographicDegrees'].extend([diff, lng, lat, 0])
    rows += 1
  print 'badrows:{}, emptyrows:{}, rows:{}'.format(badrows, emptyrows, rows)

with open(f + '.json', 'w') as outfile:
  json.dump(whales, outfile)