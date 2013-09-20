from operator import or_
from sympy.geometry import *
from sympy.core.numbers import Rational
import matplotlib.pyplot as plt
import random
import time
import csv
import sys
import json
import pdb



class Filterer(object):
  def __init__(self, radius=None, table='pickups', lat='lat', lon='lon', time='time'):
    radius = radius or 250
    self.radius = radius / 111137.60749963613 # 500 meters in degrees at 42.3 lat
    self.table = table
    self.lat = lat
    self.lon = lon
    self.time = time

  def query(self, latlons, timeranges):
    query = "select * from %s where %s" % (self.table, self.positive_where(latlons, timeranges))
    print query
    return query

  def negate_query(self, latlons, timeranges):
    query = "select * from %s where not(%s)" % (self.table, self.positive_where(latlons, timeranges))
    print query
    return query

  def positive_where(self, latlons, timeranges):
    wheres = []

    if latlons:
      locwheres = []
      for latlon in latlons:
        locwheres.append(
            "((%s - %f)^2 + (%s - %f)^2)^0.5 < %f" % (self.lat, latlon[0], self.lon, latlon[1], self.radius)
            )
      wheres.append('(%s)' % ' or '.join(locwheres))


    twheres = []
    for tr in timeranges:
      twheres.append("(%s >= '%s' and %s <= '%s')" % (self.time, tr[0], self.time, tr[1]))
    wheres.append('(%s)' % ' or '.join(twheres))

    where = ' and '.join(wheres)
    return where

with file('../interestlocations/interestpoints.csv') as f:
  dialect = csv.Sniffer().sniff(f.read(1024))
  f.seek(0)
  r = csv.reader(f, dialect)
  r.next()
  rows = [row for row in r]
  latlons = [(float(row[-2]), float(row[-1])) for row in rows]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(50, 30))
lats, lons = zip(*latlons)
r = 250/111137.60749963613
plt.bar(lats, [r]*len(lats), width=r, bottom=lons, alpha=0.1)

plt.savefig('foo.png', format='png')

       
if __name__ == '__main__':
  f = Filterer(table='pickups_oct', lat='pickup_lat', lon='pickup_long', time='pickup_time')

  # pick random data
  random.seed(0)
  months = ['10']
  days = range(1, 30)
  days = random.sample(days, 4)
  days = ['2012-10-%s' % d for d in days]
  dayranges = [['%s 00:00:01' % d, '%s 23:59:59' % d] for d in days]

  i = 0
  for day in days:
    hour = random.randint(0, 22)
    for latlon in latlons:
      if random.random() < 0.3:
        print "%d,%s,%d,%d,%f,%f" % (
            i, 
            day, hour, hour+2,
            latlon[0], latlon[1]
        )
        i += 1


  f.query(latlons[:0], dayranges)
  f.negate_query(latlons[:0], dayranges)
  exit()

    


