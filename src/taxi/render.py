from operator import or_
import matplotlib.pyplot as plt
import time
import csv
import sys
import json
import pdb



if __name__ == "__main__":
  fig = plt.figure(figsize=(50, 30))
  with file("valid_polygons.json", "r") as f:
    valid_polygons = json.loads(f.read())
    for vp in valid_polygons:
      xs, ys = zip(*vp)
      plt.plot(xs, ys)

  plt.show()

