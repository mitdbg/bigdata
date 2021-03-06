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
    '2012_04.json.gz',
    '2012_05.json.gz',
    '2012_06.json.gz',
    '2012_07.json.gz',
    '2012_08.json.gz',
    '2012_09.json.gz',
    '2012_10.json.gz',
    '2012_11.json.gz',
    '2012_12.json.gz',
    'interestpoints.csv',
    'pickups_train.csv.gz',
    'pickups_test1.csv',
    'dropoffs.csv.gz',
    'wunderground.json.gz',
    'events.csv.gz',
    'pickups_test2.csv'
  ]
  valid_files += ['test.txt']
  valid_files = [ 'pickups_test2.csv']

  if fname in valid_files or 'pickups_' in fname:
    r = HttpResponse()
    r['Content-Disposition'] = 'attachment; filename=%s' % fname
    r['X-Accel-Redirect'] = '/private/%s' % fname
    r['Content-Type'] = 'application/octet-stream'
    return r
  #return error(request, "Download Error", "Contest is over, downloads are disabled")
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
def test2(request):
  if request.method == 'POST':
    form = FinalSubmitForm(request.POST)

    if form.is_valid():
      form.save(request.user)

      return HttpResponseRedirect('/account')
  else:
    form = FinalSubmitForm()
  return render(request, 'home/prediction_test2.html', {'test2form': form})



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


def gallery(request, password):
  return render(request, 'home/gallery.html', {})
  return HttpResponseRedirect('/')

def stats(request, password):
  if password == 'imjusthereforthefood':
    try:
      npsubmissions = Submission.objects.count()
      nvsubmissions = VisSubmission.objects.count()

      nusers = User.objects.count()
      users = User.objects.all()
      from django.db import connection
      cursor = connection.cursor()
      counts = []
      cursor.execute("select date_joined::date as date, count(*) from auth_user group by date order by date")
      for row in cursor.fetchall():
        counts.append({'x':row[0].isoformat(), 'y':int(row[1])})
      cursor.close()

      data = {
        'npsubmissions': npsubmissions,
        'nvsubmissions': nvsubmissions,
        'vsubmissions': VisSubmission.objects.all(),
        'nusers': nusers,
        'users': users,
				'counts': counts
      }
      
      return render(request, 'home/stats.html', data)
    except Exception as e:
      print e
      return error(request, "whoops", str(e))
      

  return HttpResponseRedirect('/')
