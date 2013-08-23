import os

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import misaka as m
from markdown import Markdown
from home.models import *
from home.util import *



def render_md(request, mdfilepath, context=None):
  if not context:
    context = {}
  content = ""
  print os.path.abspath(".")
  with file(mdfilepath, "r") as f:
    s = f.read()
    content = m.html(s)
    #m = Markdown()
    #content = m.convert(s)
  context['content'] = content
  return render(request, "home/md_template.html", context)

def render_page(request, pagename, context=None):
  htmlfilepath = "./templates/home/%s.html" % pagename
  print htmlfilepath
  if os.path.exists(htmlfilepath):
    return render_to_response(
        'home/%s.html'%pagename, 
        context_instance=RequestContext(request))

  mdfilepath = "./templates/home/%s.md" % pagename
  print mdfilepath
  return render_md(request, mdfilepath, context)

def index(request):
  return page(request, "index")

def page(request, pagename=None):
  try:
    return render_page(request, pagename)
  except Exception as e:
    return error(request, 'Could not find page', str(e))

# This should be a context manager
def error(request, title='There was an error', msg=""):
  context = {'title': 'There was an error',  'message': msg }
  return render(request, "error.html", context)


def info(request):
  return render_md(request, "./templates/home/info.md")

def prediction(request):
  return render_md(request, "./templates/home/prediction.md")

def visualization(request):
  return render_md(request, "./templates/home/visualization.md")

def profile(request):
  return render(request, "home/user_profile.html", {})

@login_required
def submit(request):
  if request.method == 'POST':
    user = request.user
    text = request.POST.get('submission', None)
    submit_type = request.POST.get('submit_type', 1) # 1 for test
    prediction = parse(text)
    score = compute_score(prediction)

    submission = Submission(
      user = user,
      text = text,
      score = score,
      submit_type = submit_type
    )
    submission.save()
    return render(request, "home/user_profile.html", {'score': score, 'text': text})
  return render(request, "home/user_profile.html", {})


