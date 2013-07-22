import os
import sys
import time
import csv
import sys
import json


from operator import or_
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from mrjob.protocol import *
from mrjob.job import MRJob

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



class CSVProtocol(object):
  def __init__(self):
    self.nlines = 0
    self.keys = 100
    self.latidx = None
    self.lonidx = None

  def extract_start_pt(self, tup):
    lon = None
    lat = None
    for idx, col in enumerate(tup):
      if 'start' in col:
        if 'longitude' in col:
          lon = idx
        if 'latitude' in col:
          lat = idx
    if lat is None or lon is None:
      raise Error("lat/lon could not be decoded")
    self.latidx = lat
    self.lonidx = lon



  def read(self,line):
    arr = line.split(",")
    spt = None
    if self.nlines == 0:
      self.extract_start_pt(arr)

    try:
      arr[self.latidx] = float(arr[self.latidx])
      arr[self.lonidx] = float(arr[self.lonidx])
      spt = (arr[self.lonidx], arr[self.latidx])
    except ValueError:
      pass
    except IndexError:
      pass

    key = self.nlines % self.keys
    self.nlines += 1
    return spt, arr
  
  def write(self, key, value):
    return ",".join(map(str, value))





class MRFilter(MRJob):

  INPUT_PROTOCOL = CSVProtocol
  OUTPUT_PROTOCOL = CSVProtocol

  def mapper_init(self):
    try:
      #awskey = os.environ["AWS_ACCESS_KEY"]
      #awssecret = os.environ["AWS_SECRET_KEY"]
      awskey="AKIAIL7JTKBN7BYCF5RA"
      awssecret="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"
    except:
      print "set envron vars"
      exit()
    conn = S3Connection(awskey, awssecret)
    b = conn.get_bucket("mitbigdata")
    key = b.get_key("taxi/valid_polygons.json")
    data = key.read()
    conn.close()
    self.valid_polygons = json.loads(data)
    self.nerrors = 0

  def mapper(self, spt, tup):
    if spt is None:
      self.nerrors += 1
      print tup
      if self.nerrors > 20:
        raise e
      yield key, tup

    else:
      f = lambda vp: pip(spt[0], spt[1], vp)
      valid = reduce(or_, map(f, self.valid_polygons))
      if valid:
        yield key, tup


if __name__ == "__main__":
#  MRJob.run()




  fname = sys.argv[1]
  parser = CSVProtocol()
  nerrors = 0
  with file("valid_polygons.json", "r") as f:
    valid_polygons = json.loads(f.read())

  with file(fname, "r") as f:
    with file("%s.filtered" % fname, "w") as fout:
      for lineidx, line in enumerate(f):
        try:
          (spt, tup) = parser.read(line)
        except Exception as e:
          print e
          print tup
          continue



        if spt is None:
          nerrors += 1
          print tup
          if nerrors > 20:
            raise Error()
          fout.write(parser.write(spt, tup))
        else:
          f = lambda vp: pip(spt[0], spt[1], vp)
          valid = reduce(or_, map(f, valid_polygons))
          if valid:
            fout.write(parser.write(spt, tup))

        if lineidx % 10000 == 0:
          fout.flush()





