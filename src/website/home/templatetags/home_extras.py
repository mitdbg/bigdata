from django.template.base import Library
from home.models import *

print "hi"

register = Library()
@register.inclusion_tag('home/infobox.html')
def infobox(user):
  return {'user': user }


@register.inclusion_tag('home/leaderboard.html', takes_context=True)
def leaderboard(context):
  topk = Submission.objects.order_by('score')[:10]
  return {'submissions': topk}
