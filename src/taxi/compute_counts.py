import sys, os
from dateutil import parser
from sqlalchemy import *


def row2clause(row):
  latlon, stime, etime = tuple(row)
  lat, lon = tuple(latlon)
  q = " (((pickup_lat - %f)^2 + (pickup_long - %f)^2)^0.5 <= %f and (pickup_time >= '%s'::timestamp) and (pickup_time <= '%s'::timestamp))"
  return q % (lat, lon, 250./111137.60749963613, stime, etime)

def parseline(line):
  arr = line.split(',')
  arr[0] = int(arr[0])
  arr[1] = parser.parse(arr[1])
  arr[2] = parser.parse(arr[2])
  arr[3] = float(arr[3])
  arr[4] = float(arr[4])
  return (arr[0], (arr[3], arr[4]), arr[1], arr[2])


if len(sys.argv) < 3:
  print "usage: python compute_counts.py <timespan file>  <database table with data>"
  print "tables: pickups_train, pickups_test1, pickups_test2"
  exit()

db = create_engine("postgresql://localhost:5432/bigdata")
fname = sys.argv[1]
table = sys.argv[2]


with file(fname) as f:
  rows = map(parseline, f)
  for row in rows:
    id = row[0]
    data = row[1:]
    where = row2clause(data)
    q = "select count(*) from %s where %s" % (table, where)
    print id, db.execute(q).fetchone()[0]
