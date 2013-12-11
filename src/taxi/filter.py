from operator import or_
from sqlalchemy import *
import matplotlib.pyplot as plt
from datetime import *
from collections import *
import random
import math
import numpy as np
import time
import csv
import sys
import json
import pdb

def block_iter(l, nblocks=2):
    """
    partitions l into nblocks blocks and returns generator over each block
    @param l list
    @param nblocks number of blocks to partition l into
    """
    blocksize = int(math.ceil(len(l) / float(nblocks)))
    i = 0
    while i < len(l):
        yield l[i:i+blocksize]
        i += blocksize      
 

class Filterer(object):
  def __init__(self, radius=None, table='pickups', lat='lat', lon='lon', time='time'):
    radius = radius or 250
    self.radius = radius / 111137.60749963613 # 500 meters in degrees at 42.3 lat
    self.table = table
    self.lat = lat
    self.lon = lon
    self.time = time

  # @param blocks array of block
  #block: [lat, lon, starttime, endtime]
  def query(self, blocks):
    query = "select * from %s where %s" % (self.table, self.positive_where(blocks))
    return query

  def negate_query(self, blocks):
    query = "select * from %s where not(%s)" % (self.table, self.positive_where(blocks))
    print query
    return query
  
  def count(self, block, db=None):
    if not db:
      db = create_engine("postgresql://localhost:5432/bigdata")
    lat, lon, s, e = tuple(block)
    q = """select count(*) from %s where
     (((%s - %f)^2 + (%s - %f)^2)^0.5 < %f) and (%s >= '%s' and %s <= '%s')""" % (
        self.table,
        self.lat, lat, self.lon, lon, self.radius,
        self.time, s, self.time, e
      )
    print q
    row = db.execute(q).fetchone()
    return row[0]

  def positive_where(self, blocks):
    wheres = []

    if blocks:
      for block in blocks:
        lat, lon, s, e = tuple(block)
        wheres.append(
          """((((%s - %f)^2 + (%s - %f)^2)^0.5 < %f) and (%s >= '%s' and %s <= '%s'))""" % (
            self.lat, lat, self.lon, lon, self.radius,
            self.time, s, self.time, e)
        )

    return ' or '.join(wheres)

    twheres = []
    for tr in timeranges:
      twheres.append("(%s >= '%s' and %s <= '%s')" % (self.time, tr[0], self.time, tr[1]))
    wheres.append('(%s)' % ' or '.join(twheres))

    where = ' and '.join(wheres)
    return where


db = create_engine("postgresql://localhost:5432/bigdata")
fil = Filterer(table='pickups_train', lat='pickup_lat', lon='pickup_long', time='pickup_time')
with file('data/test1_2hrspans.txt', 'r') as f:
  blocks = []
  for l in f:
    arr = l.split(',')
    from dateutil import parser
    s = parser.parse(arr[1])
    e = parser.parse(arr[2])
    lat = float(arr[3])
    lon = float(arr[4])
    blocks.append((lat, lon, s, e))
    if (arr[0] == '656'):
      count = fil.count((lat, lon, s, e), db)
      print "%s\t%s" % (arr[0], count)






exit()

with file('../interestlocations/interestpoints.csv') as f:
  dialect = csv.Sniffer().sniff(f.read(1024))
  f.seek(0)
  r = csv.reader(f, dialect)
  r.next()
  rows = [row for row in r]
  latlons = [(float(row[-2]), float(row[-1])) for row in rows]
  locnames = [row[0] for row in rows]


#fig = plt.figure(figsize=(50, 30))
#lats, lons = zip(*latlons)
#r = 250/111137.60749963613
#plt.bar(lats, [r]*len(lats), width=r, bottom=lons, alpha=0.1)
#
#plt.savefig('foo.png', format='png')


def row2clause(row):
  latlon, name, stime, etime = tuple(row)
  lat, lon = tuple(latlon)
  q = " (((pickup_lat - %f)^2 + (pickup_long - %f)^2)^0.5 <= %f and (pickup_time >= '%s'::timestamp) and (pickup_time <= '%s'::timestamp))"
  print stime, etime, name
  return q % (lat, lon, 250./111137.60749963613, stime, etime)

def rows2clause(dt, rows):
  stime, etime = dt

  loc2clause = lambda row: "(((pickup_lat - %f)^2 + (pickup_long - %f)^2)^0.5 <= %f)"  % (row[0][0], row[0][1], 250./111137.60749963613)
  clause = " or ".join(map(loc2clause, rows))
  tclause = "('%s' <= pickup_time and pickup_time <= '%s')" % (stime, etime)
  where = "(%s and (%s))" % (tclause, clause) 
  return where


def partition(items, keyf, value=lambda d:d):
  ret = defaultdict(list)
  for item in items:
    ret[keyf(item)].append(value(item))
  return ret

def rowsnotzero((dt, rows)):
  where = rows2clause(dt, rows)
  q = "select count(*) from pickups_train where %s" % where
  return db.execute(q).fetchone()[0] > 0

db = create_engine("postgresql://localhost:5432/bigdata")
rows = json.load(file('./timeslots'))
partitions = partition(rows, lambda r: (r[2], r[3])).items()
random.shuffle(partitions)
test1rows = partitions[:len(partitions)/2]
test2rows = partitions[len(partitions)/2:]

test1rows.sort(key=lambda r: r[0])
test1rows = filter(rowsnotzero, test1rows)
test2rows.sort(key=lambda r: r[0])
test2rows = filter(rowsnotzero, test2rows)
for dt, rows in test1rows:
  where = rows2clause(dt, rows)
  q = "select count(*) from pickups_train where %s" % where
  print dt, len(rows), db.execute(q).fetchone()
  q = "insert into pickups_test1 select * from pickups_train where %s" % where
  db.execute(q)
  q = "delete from pickups_train where %s" % where
  db.execute(q)

print 

for dt, rows in test2rows:
  where = rows2clause(dt, rows)
  q = "select count(*) from pickups_train where %s" % where
  print dt, len(rows), db.execute(q).fetchone()
  q = "insert into pickups_test2 select * from pickups_train where %s" % where
  db.execute(q)
  q = "delete from pickups_train where %s" % where
  db.execute(q)

# turn them into 
def write_test_csv(testrows, fname):
  output = []
  i = 0
  for dt, rows in testrows:
    for row in rows:
      output.append((i, dt[0], dt[1], row[0][0], row[0][1]))
      i += 1

  with open(fname, 'wb') as csvfile:
    w = csv.writer(csvfile, delimiter=',')
    map(w.writerow, output)

write_test_csv(test1rows, 'test1.txt')
write_test_csv(test2rows, 'test2.txt')




exit()

# setup delete

for i, block in enumerate(block_iter(rows[:len(rows)/2], 50)):
  where = ' or '.join(map(row2clause, rows))
  q = "insert into pickups_test1 select * from pickups where %s" % where
  print i, len(block)
  exit()
  db.execute(q)

for i, block in enumerate(block_iter(rows[len(rows)/2:], 50)):
  where = ' or '.join(map(row2clause, rows))
  q = "insert into pickups_test2 select * from pickups where %s" % where
  print i, len(block)
  db.execute(q)

for i, block in enumerate(block_iter(rows, 100)):
  where = ' or '.join(map(row2clause, rows))
  q = "delete from pickups_train where %s" % where
  print i, len(block)
  db.execute(q)

exit()
       
if __name__ == '__main__':
  f = Filterer(table='pickups', lat='pickup_lat', lon='pickup_long', time='pickup_time')

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

    


