import os

from django.http import HttpResponse
from django.shortcuts import render
from markdown import Markdown


def render_md(request, mdfilepath, context=None):
  if not context:
    context = {}
  content = ""
  print os.path.abspath(".")
  with file(mdfilepath, "r") as f:
    s = f.read()
    m = Markdown()
    content = m.convert(s)
  context['content'] = content
  return render(request, "home/index_template.html", context)


def index(request):
  return render_md(request, "./templates/home/index.md")

def info(request):
  return render_md(request, "./templates/home/info.md")

def prediction(request):
  return render_md(request, "./templates/home/prediction.md")

def visualization(request):
  return render_md(request, "./templates/home/visualization.md")
