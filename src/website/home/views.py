import os

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import misaka as m
from markdown import Markdown
from home.models import *
from home.util import *
from home.forms import *



def render_page(request, pagename, context=None):
  htmlfilepath = "./templates/home/%s.html" % pagename
  if os.path.exists(htmlfilepath):
    return render_to_response(
        'home/%s.html'%pagename, 
        context_instance=RequestContext(request))

  return error(request, "Whoops", "could not find %s" % pagename)

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


def visualization(request):
  visform = VisForm()
  return render(request, "home/visualization.html",
      {'visform': visform})

@login_required
def download(request, fname=None):
  valid_files = [
      'jan', 'feb', 'mar', 'apr', 'may', 'jun', 
      'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
  ]
  valid_files = ['%s.tar.gz' % f for f in valid_files] + ['test.txt']

  if fname in valid_files:
    r = HttpResponse()
    r['Content-Disposition'] = 'attachment; filename=%s' % fname
    r['X-Accel-Redirect'] = '/twitter/%s' % fname
    return r
  return error(request, "Download Error", "Could not find downloadable file %s" % fname)

@login_required
def profile(request):
  form = SubmitForm()
  visform = VisForm()
  return render(request, "home/user_profile.html", {
    'test1form': form,
    'visform': visform
    })

@login_required
def test1(request):
  if request.method == 'POST':
    form = SubmitForm(request.POST)

    if form.is_valid():
      form.save(request.user)

      return HttpResponseRedirect('/account')
  else:
    form = SubmitForm()
  return render(request, 'home/prediction_test1.html', {'test1form': form})



@login_required
def submit_vis(request):
  if request.method == 'POST':
    form = VisForm(request.POST)
    if form.is_valid():
      form.save(request.user)
      return HttpResponseRedirect('/account#vis')
  else:
    form = VisForm()
  return render(request, 'home/visualization.html', { 'visform': form })

