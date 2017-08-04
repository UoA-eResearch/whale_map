#!/usr/bin/env python

import sys
import numpy as np
from matplotlib import pyplot as plt
import cv2

files = sys.argv[1:]

shape = (332, 316)

with open('pss25lats_v3.dat') as f:
  data = np.fromfile(f, dtype=np.dtype("<i4"))
lats = np.reshape(data, shape) / 1E5

with open('pss25lons_v3.dat') as f:
  data = np.fromfile(f, dtype=np.dtype("<i4"))
lons = np.reshape(data, shape) / 1E5

#Each array location (i, j) contains the latitude/longitude value at the center of the corresponding data grid cells.

for filename in files:
  with open(filename) as f:
    header = f.read(300)
    data = np.fromfile(f, dtype=np.uint8)
  data = np.reshape(data, shape)
  data = np.where(data < 251, data, 0) # Filter to just ice
  contours, hierarchy = cv2.findContours(data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  mask = np.zeros(data.shape[:2], np.uint8)
  cv2.drawContours(mask, contours, -1, 255, -1)

  for c in contours:
    if len(c) > 1:
      for pair in c[0]:
        lon = lons[pair[0], pair[1]]
        lat = lats[pair[0], pair[1]]

  fig = plt.figure()
  fig.canvas.set_window_title(filename)
  plt.imshow(mask, cmap='gray')

plt.show()
