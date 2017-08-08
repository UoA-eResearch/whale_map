#!/usr/bin/env python

import sys
import numpy as np
import datetime
import time
from matplotlib import pyplot as plt
import cv2
import json

files = sys.argv[1:]

shape = (332, 316)

with open('pss25lats_v3.dat') as f:
  data = np.fromfile(f, dtype=np.dtype("<i4"))
lats = np.reshape(data, shape) / 1E5

with open('pss25lons_v3.dat') as f:
  data = np.fromfile(f, dtype=np.dtype("<i4"))
lons = np.reshape(data, shape) / 1E5

#Each array location (i, j) contains the latitude/longitude value at the center of the corresponding data grid cells.

polys = []
s = time.time()

for filename in files:
  with open(filename) as f:
    header = f.read(300)
    data = np.fromfile(f, dtype=np.uint8)
  data = np.reshape(data, shape)
  data = np.where(data < 251, data, 0) # Filter to just ice
  contours, hierarchy = cv2.findContours(data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  start = datetime.date(int(header[131:135]), int(header[135:137]), int(header[137:139]))
  end = start + datetime.timedelta(days=1)
  startS = start.isoformat() + 'T00:00:00Z'
  endS = end.isoformat() + 'T00:00:00Z'

  for c in contours:
    if len(c) > 10:
      positions = []
      for pair in c:
        lon = lons[pair[0][1], pair[0][0]]
        lat = lats[pair[0][1], pair[0][0]]
        positions.extend([lon, lat, 0])
      polys.append({
        "interval" : "{}/{}".format(startS, endS),
        "cartographicDegrees": positions
      })
  print("{} done, {}s elapsed".format(filename, round(time.time() - s)))

with open('seaice.json', 'w') as outfile:
  json.dump(polys, outfile)
