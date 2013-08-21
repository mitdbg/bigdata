from django.template.base import Library

print "hi"

register = Library()
@register.inclusion_tag('home/infobox.html')
def infobox(user):
  return {'user': user }
