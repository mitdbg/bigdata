
from home.models import *
from home.util import *


for s in  Submission.objects.all():
  score = compute_score(parse(s.text))
  print s.user, score
