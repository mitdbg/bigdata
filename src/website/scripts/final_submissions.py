from header import *
from django.core.mail import send_mail, send_mass_mail

import sys
sys.path.append('..')

from sqlalchemy import *
from home.util import *
from home.models import *

last_submits = {}
  

db = create_engine("postgresql://challenge:imjusthereforthefood@localhost:5432/challenge")

q = """SELECT email, s.text , tstamp
FROM  auth_user, home_submission as s
WHERE submit_type = 2 and tstamp < '2014-01-21' and auth_user.id = s.user_id
ORDER BY email asc, tstamp desc
"""
res = db.execute(q)
for email, text, tstamp in res:
  if email not in last_submits:
    last_submits[email] = (text, tstamp)

scores = {}
for email, (text, tstamp) in last_submits.items():
  try:
    score = compute_score(parse(text), TEST2_COUNTS)
    errs = compute_score_breakdown(parse(text), TEST2_COUNTS)
    scores[email] = (score, errs, tstamp)
  except Exception as e:
    print email
    print e

pairs = sorted(scores.items(), key=lambda p: p[1], reverse=True)
for email, (score, errs, tstamp) in pairs:
  print '%s\t%.7f\t%s' % (tstamp, score, email)
  
cols = []
for email, (score, errs, tstamp) in pairs:
  cols.append([email] + errs)
cols.insert(0, ['locid'] + range(len(cols[0]) - 1))

rows = zip(*cols)
for row in rows:
  print ','.join(map(str, row))
  
