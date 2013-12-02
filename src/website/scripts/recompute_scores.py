from header import *

update = False
if len(sys.argv) > 1:
  if sys.argv[1] == 'update':
    raw_input("updating are you sure?  ctrl-c to abort!")
    update = True

scores = []
for s in  Submission.objects.all():
  score = compute_score(parse(s.text))
  s.score = score
  s.save()
  scores.append((s.user, score))

scores.sort(key=lambda p: p[1], reverse=True)
for u,score in scores:
  print u, score
