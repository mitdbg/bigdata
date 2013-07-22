from operator import or_
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
        alpha = 0.2
        plt.plot(xs, ys, c=color, alpha=alpha)
        x = (max(xs)-min(xs))/2. + min(xs)
        y = (max(ys)-min(ys))/2. + min(ys)
        plt.text(x, y, tract, color=color, alpha=0.4)

    boston_polygons = filter(bool, map(pts2poly, boston_polygons))
    boston_polygons = merge_polygons(boston_polygons)

  return boston_polygons


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
      "noends": 0,
      "nlines": 0
      }
  fname = sys.argv[1]

  
  valid_polygons = [zip(*p.boundary.xy) for p in boston_polygons]
  with file("valid_polygons.json", "w") as f:
    f.write(json.dumps(valid_polygons))


  plt.savefig("./boston_tracts.pdf", format="pdf")
