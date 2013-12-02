import os
import sys
sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from home.models import *
from home.util import *

scores = []
for s in  Submission.objects.all():
  score = compute_score(parse(s.text))
  scores.append((s.user, score))

scores.sort(key=lambda p: p[1], reverse=True)
for u,score in scores:
  print u, score
