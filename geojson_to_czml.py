import json

positions = []
months = ["201510", "201511", "201512", "201601", "201602", "201603", "201604"]
for i in range(0, len(months) - 1):
  f = open('seaice_geojson/extent_S_{}_polygon.geojson'.format(months[i]))
  geo = json.load(f)
  start = '{}-{}-01T00:00:00Z'.format(months[i][0:4], months[i][4:6])
  end = '{}-{}-01T00:00:00Z'.format(months[i+1][0:4], months[i+1][4:6])
  primary_feature = geo['features'][0]['geometry']['coordinates'][0]
  coords = []
  for pair in primary_feature:
    coords.extend([pair[0], pair[1], 0])
  positions.append({"interval" : "{}/{}".format(start, end),
                    "cartographicDegrees" : coords})
with open('seaice.json', 'w') as outfile:
  json.dump(positions, outfile)