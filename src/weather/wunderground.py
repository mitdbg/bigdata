import requests
import time
import json
from pyquery import PyQuery as pq

URL = "http://www.wunderground.com/history/airport/KBOS/2012/%d/%d/DailyHistory.html?req_city=Cambridge&req_state=MA&req_statename=Massachusetts"
URL = "http://api.wunderground.com/api/57929e89bff6b6d4/history_%s/q/MA/Boston.json"
FNAME = "./wunderground.json"
db = []

months = [5,6,7,8,9]
days = range(1,32)

for month in months:
  for day in days:
    date = "2012%02d%02d" % (month, day)
    url = URL % date
    html = requests.get(url).content
    try:
      data = json.loads(html)
      db.append(data)
    except:
      print date
      pass

with file(FNAME, 'w') as f:
  f.write(json.dumps(db))
