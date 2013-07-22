from operator import or_
from sympy.geometry import *
from sympy.core.numbers import Rational
import matplotlib.pyplot as plt
import time
import csv
import sys
import json
import pdb


def pts2poly((valid, tract, pts)):
  from shapely.geometry import Polygon
  if valid:
    return Polygon(pts)

def merge_polygons(polygons):
  complete = None
  for polygon in polygons:
    if complete:
      complete = complete.union(polygon)
    else:
      complete = polygon
  return complete

def get_boston_polygons(fname, fig=None):

  with file(fname, "r") as f:
    boston_polygons = json.loads(f.read())
    if fig:
      for (valid, tract, polygon) in boston_polygons:
        xs, ys = zip(*polygon)
        color = valid and "black" or "red"
        alpha = 0.1
        plt.plot(xs, ys, c=color, alpha=alpha)
        x = (max(xs)-min(xs))/2. + min(xs)
        y = (max(ys)-min(ys))/2. + min(ys)
        plt.text(x, y, tract, color=color, alpha=0.3)

    boston_polygons = filter(bool, map(pts2poly, boston_polygons))
    boston_polygons = merge_polygons(boston_polygons)

  return boston_polygons



class Point:
  def __init__(self, x,y):
    self.x = x
    self.y = y

def tuple_to_pt(tup):
  spt = ept = None
  try:
    slon, slat = float(tup[3]), float(tup[4])
    spt = Point(slon, slat)
  except ValueError:
    print tup

  try:
    elon, elat = float(tup[-3]), float(tup[-2])
    ept = Point(elon, elat)
  except ValueError:
    ept = None
  return spt, ept


def taxi_locations(fname):
  with file(fname, "r") as f:
    dialect = csv.Sniffer().sniff(f.read(5000))
    f.seek(0)
    reader = csv.reader(f, dialect)
    for nlines, tup in enumerate(reader):
      if nlines is 0:
        yield None, None, tup
        continue
      
      spt, ept = tuple_to_pt(tup)

      yield spt, ept, tup



def valid_taxi_tuples(fname, stats, valid_polygons, boundbox, fig=None, block=1000):
  last = start = time.time()
  locs = enumerate(taxi_locations(fname))
  for nlines, (spt, ept, tup) in locs:
    if not spt and not ept and nlines is 0:
      yield tup
    if not spt: 
      continue

    f = lambda vp: pip(spt.x, spt.y, vp)
    valid = reduce(or_, map(f, valid_polygons))
    color = valid and "green" or "red"
    stats["nlines"] = nlines
    stats["ngood"] += valid
    stats["rejected"] += (not valid)
    stats["noends"] += (not ept)

    if valid:
      yield tup

    if fig and spt.x >= boundbox[0][0] and spt.x <= boundbox[0][1] and spt.y >= boundbox[1][0] and spt.y <= boundbox[1][1]:
      lon = min(max(spt.x, boundbox[0][0]), boundbox[0][1])
      lat = min(max(spt.y, boundbox[1][0]), boundbox[1][1])
      plt.scatter(lon, lat, c=color, s=5, alpha=0.3, lw=0)

    if nlines % block == 0:
      total = time.time() - start
      cost = time.time() - last
      print "%.2f\t%.2f\t%d\t%d\t%d" % (total, cost, stats["nlines"], stats["rejected"], stats["noends"])
      last = time.time()

  stats["totalcost"] = time.time() - start


def point_inside_polygon(x,y,poly):
  n = len(poly)
  inside =False

  p1x,p1y = poly[0]
  for i in range(n+1):
    p2x,p2y = poly[i % n]
    if y > min(p1y,p2y):
      if y <= max(p1y,p2y):
        if x <= max(p1x,p2x):
          if p1y != p2y:
            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
          if p1x == p2x or x <= xinters:
            inside = not inside
    p1x,p1y = p2x,p2y

  return inside
pip = point_inside_polygon


 
if __name__ == "__main__":

  fig = plt.figure(figsize=(50, 30))
  boston_polygons = get_boston_polygons("./boston_polygons.json", fig)
  bound = boston_polygons.bounds
  xr = bound[2]-bound[0]
  yr = bound[3]-bound[1]
  bound = [[bound[0]-xr/2, bound[2]+xr/2], [bound[1]-yr/2, bound[3]+yr/2]]

  block = 1000
  stats = {
      "rejected": 0,
      "ngood": 0,
      "noends": 0,
      "nlines": 0
      }
  fname = sys.argv[1]

  
  valid_polygons = [zip(*p.boundary.xy) for p in boston_polygons]
  with file("valid_polygons.json", "w") as f:
    f.write(json.dumps(valid_polygons))


  with file("valid_polygons.json", "r") as f:
    valid_polygons = json.loads(f.read())

  if fig:
    for p in boston_polygons:
      xy = p.boundary.xy
      plt.plot(xy[0], xy[1], c="green", alpha=0.2)


  
  print "running"
  with file("%s.filtered" % fname, "w") as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    valid_locs = valid_taxi_tuples(fname, stats, valid_polygons, bound, 
        fig, block)
    
    for tup in valid_locs:
      writer.writerow(tup)


  start = time.time()
  plt.savefig("map_filtered.pdf", format="pdf")
  print "render:   \t%.4f" % (time.time() - start)
  for key in stats:
    print "%s\t%d" % (key, stats[key])
