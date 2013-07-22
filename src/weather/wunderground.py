import requests
import bsddb3
import time
from pyquery import PyQuery as pq

URL = "http://www.wunderground.com/history/airport/KBOS/2012/%d/%d/DailyHistory.html?req_city=Cambridge&req_state=MA&req_statename=Massachusetts"
FNAME = "./wunderground.bdb"
db = bsddb3.hashopen(FNAME)


months = [6,7]
days = range(1,32)

for month in months:
  for day in days:
    url = URL % (month, day)
    html = requests.get(url).content
    db["%d/%d" % (month, day)] = html
    time.sleep(10)

db.close()
