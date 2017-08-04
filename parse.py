#!/usr/bin/env python

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
  reader.fieldnames = [name.lower() for name in reader.fieldnames]
  emptyrows = 0
  rows = 0
  for row in reader:
    if not row['ptt']:
      emptyrows += 1
      continue
    if 'date_time' not in row:
      row['date_time'] = "{} {}".format(row['date'], row['time'])
    dt = parse(row['date_time'], dayfirst=True)
    lat = float(row['latitude'])
    lng = float(row['longitude'])
    if row['ptt'] not in whales:
      epoch = dt
      epochIso = dt.isoformat() + 'Z'
      whales[row['ptt']] = {'epoch': epochIso, 'cartographicDegrees': [0, lng, lat, 0]}
    else:
      diff = dt - epoch
      diff = int(diff.total_seconds())
      whales[row['ptt']]['cartographicDegrees'].extend([diff, lng, lat, 0])
    rows += 1
  print 'emptyrows:{}, rows:{}'.format(emptyrows, rows)

with open(f + '.json', 'w') as outfile:
  json.dump(whales, outfile)
