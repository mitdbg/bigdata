from operator import or_
from sympy.geometry import *
from sympy.core.numbers import Rational
from sqlalchemy import *
import matplotlib.pyplot as plt
from collections import *
import random
import math
import numpy as np
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
  
  def count(self, latlon, timerange):
    db = create_engine("postgresql://localhost:5432/bigdata")
    q = """select count(*) from %s where
     (((%s - %f)^2 + (%s - %f)^2)^0.5 < %f) and (%s >= '%s' and %s <= '%s')""" % (
        self.table,
        self.lat, latlon[0], self.lon, latlon[1], self.radius,
        self.time, timerange[0], self.time, timerange[1]
      )
    row = db.execute(q).fetchone()
    return row[0]

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


fig = plt.figure(figsize=(140, 40))

db = create_engine('postgresql://localhost:5432/bigdata')
q = "select distinct date_trunc('hour', pickup_time) as hour from pickups_lean where pickup_time > '2012-06-01' order by hour "
hours = filter(bool, [r[0] for r in db.execute(q)])
blocksize = int(math.floor(len(hours) / 20))
ticks = [hours[blocksize * i] for i in xrange(20)]



latlons = latlons[:10]
for i, latlon in enumerate(latlons):
  subplot = fig.add_subplot(len(latlons), 1, i)
  q = "select count(*) as count, date_trunc('hour', pickup_time) as hour from pickups_lean where ((pickup_lat - %f)^2 + (pickup_long - %f)^2)^0.5 < %f group by hour order by hour asc" % (latlon[0], latlon[1], 250/111137.60749963613)
  res = db.execute(q)
  avgcounts = defaultdict(list)
  rows = {}
  for r in res:
    avgcounts[r[1].hour].append(r[0])
    rows[r[1]] = r[0]

  for k in avgcounts.keys():
    if avgcounts[k]:
      avgcounts[k] = np.mean(avgcounts[k])
    else:
      avgcounts[k] = 0

  ys = [rows.get(h,0) for h in hours]

  xs = hours
  subplot.set_xticks(ticks)

  subplot.plot(xs, ys, alpha=0.2, c="grey")


  ys = [y - avgcounts.get(h.hour, 0) for y in ys]
  smoothavg = [avgcounts.get(h.hour, 0) for h in hours]
  smoothed2 = []
  smoothed4 = []
  for i in xrange(len(ys)):
    smoothed2.append(np.mean(ys[i:i+2]))
    smoothed4.append(np.mean(ys[i:i+4]))
  subplot.plot(xs, ys, alpha=0.2, c="grey")
  subplot.plot(xs, smoothavg, alpha=0.2, c="blue")
  subplot.plot(xs, smoothed2, alpha=0.2, c="black")
  subplot.plot(xs, [1]*len(xs), alpha=0.1)
plt.savefig('foo.png', format='png')
exit()


   


fig = plt.figure(figsize=(50, 30))
lats, lons = zip(*latlons)
r = 250/111137.60749963613
plt.bar(lats, [r]*len(lats), width=r, bottom=lons, alpha=0.1)

plt.savefig('foo.png', format='png')

       
if __name__ == '__main__':
  f = Filterer(table='pickups_6_test', lat='pickup_lat', lon='pickup_long', time='pickup_time')

  # pick random data
  random.seed(0)
  months = ['10']
  days = range(1, 30)
  days = random.sample(days, 4)
  days = ['2012-06-%s' % d for d in days]
  dayranges = [['%s 00:00:01' % d, '%s 23:59:59' % d] for d in days]

  i = 0
  results = []
  for day in days:
    hour = random.randint(0, 22)
    for latlon in latlons:
      if random.random() < 0.3:
        pt = "%d,%s,%d,%d,%f,%f" % (
            i, 
            day, hour, hour+2,
            latlon[0], latlon[1]
        )
        results.append(f.count(latlon, ['%s %d:00:00' % (day, hour), '%s %d:59:59' % (day, hour+1)]))
        i += 1

  
  for i, r in enumerate(results):
    print i,r

  f.query(latlons[:0], dayranges)
  f.negate_query(latlons[:0], dayranges)
  exit()

    


