from django.template.base import Library
from home.models import *

print "hi"

register = Library()
@register.inclusion_tag('home/infobox.html')
def infobox(user):
  return {'user': user }


@register.inclusion_tag('home/leaderboard.html', takes_context=True)
def leaderboard(context):
  uids = set()
  topk = []
  for s in Submission.objects.order_by('-score'):
    if len(uids) >= 10:
      break
    if s.user.id in uids:
      continue
    topk.append(s)
    uids.add(s.user.id)
    if len(topk) > 8:
      break
  return {'submissions': topk}


